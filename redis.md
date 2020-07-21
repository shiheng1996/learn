### redis 分布式锁

```Java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.script.RedisScript;
import org.springframework.stereotype.Component;

import java.util.Collections;
import java.util.concurrent.TimeUnit;

@Component
public class RedisLockSingle {

    private static final Logger log = LoggerFactory.getLogger(RedisLockSingle.class);

    @Autowired
    private RedisTemplate redisTemplate;
    public   boolean tryGetDistributedLock(String lockKey, String requestId, long expireTime,long acquireTimeout) {
        boolean res;
        long endTime=System.currentTimeMillis()+acquireTimeout;
        while (System.currentTimeMillis()<endTime){
            //如果获取锁没有超时，则加锁
            Object o = redisTemplate.opsForValue().get(lockKey);
//            log.info(" redis lockKey {} value {} ",lockKey,o);
            res=redisTemplate.opsForValue().setIfAbsent(lockKey, requestId, expireTime, TimeUnit.MILLISECONDS);
            if(res){
                log.info("set redis lock success Key {} value {} ",lockKey,o);
                return res;
            }
        }
        return false;
    }
    //释放锁
    public  boolean releaseDistributedLock(String lockKey, String requestId) {
        String script = "if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) else return 0 end";
        //Object result = jedis.eval(script, Collections.singletonList(lockKey), Collections.singletonList(requestId));
        log.info("开始删除锁: "+Thread.currentThread().getName());
        boolean execute = (boolean)redisTemplate.execute(RedisScript.of(script, Boolean.class), Collections.singletonList(lockKey), requestId);
        log.info("删除锁的结果："+execute+"||"+Thread.currentThread().getName());
        return execute;
    }
}
```
