# redis 持久化
## aof
* 原理: 将Reids的操作日志以追加的方式写入文件
* 配置: appendfsync always 每次有数据修改发生时都会写入AOF文件,appendfsync everysec  每秒钟同步一次，该策略为AOF的缺省策略,appendfsync no  从不同步。高效但是数据不会被持久化
* aof 文件过大处理: 执行BGREWRITEAOF文件重写操作，重写会创建一个当前 AOF 文件的体积优化版本,优化重写重复命令或者可以合并的命令
## rdb
* 原理: 将Reids在内存中的数据库记录定时dump到磁盘上的RDB持久化
* 配置: save m n 表示m秒内数据集存在n次修改时，自动触发bgsave。
# redis 集群
## 主从模式
### 配置
从节点 redis.conf 配置
replicaof 主ip 6379
### 工作机制
-  从服务器连接主服务器，发送SYNC命令； 
-  主服务器接收到SYNC命名后，开始执行BGSAVE命令生成RDB文件并使用缓冲区记录此后执行的所有写命令； 
-  主服务器BGSAVE执行完后，向所有从服务器发送快照文件，并在发送期间继续记录被执行的写命令； 
-  从服务器收到快照文件后丢弃所有旧数据，载入收到的快照； 
-  主服务器快照发送完毕后开始向从服务器发送缓冲区中的写命令； 
-  从服务器完成对快照的载入，开始接收命令请求，并执行来自主服务器缓冲区的写命令；
### 特点
* 主数据库可以进行读写操作，当读写操作导致数据变化时会自动将数据同步给从数据库
* 从数据库一般都是只读的，并且接收主数据库同步过来的数据
* 一个master可以拥有多个slave，但是一个slave只能对应一个master
* slave挂了不影响其他slave的读和master的读和写，重新启动后会将数据从master同步过来
* master挂了以后，不影响slave的读，但redis不再提供写服务，master重启后redis将重新对外提供写服务
* master挂了以后，不会在slave节点中重新选一个master

## sentinel模式
## cluster模式


# redis 分布式锁

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
