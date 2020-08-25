### redis 持久化
#### aof
* 原理: 将Reids的操作日志以追加的方式写入文件
* 配置: appendfsync always 每次有数据修改发生时都会写入AOF文件,appendfsync everysec  每秒钟同步一次，该策略为AOF的缺省策略,appendfsync no  从不同步。高效但是数据不会被持久化
* aof 文件过大处理: 执行BGREWRITEAOF文件重写操作，重写会创建一个当前 AOF 文件的体积优化版本,优化重写重复命令或者可以合并的命令
#### rdb
* 原理: 将Reids在内存中的数据库记录定时dump到磁盘上的RDB持久化
* 配置: save m n 表示m秒内数据集存在n次修改时，自动触发bgsave。
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
