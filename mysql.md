# 存储引擎
## innodb与myisam区别
|  innodb   | myisam  |
|  ----  | ----  |
| 支持事务  | 不 |
| 支持行锁,表锁  | 不能 |
|支持崩溃修复能力和并发控制|不能|
|  B+Tree表数据文件和索引文件是分离的，索引文件仅保存数据记录的磁盘地址(聚集索引)  |  B+Tree表数据文件本身就是主索引，叶节点data域保存了完整的数据记录(非聚集索引) |
| 适合更新和删除比较多的表 | 适合查询和插入比较多的表 |

# 索引
## 索引实现 
### hash索引
1. 实现
键值 key 通过 Hash 映射找到桶 bucket。在这里桶（bucket）指的是一个能存储一条或多条记录的存储单位。一个桶的结构包含了一个内存指针数组，桶中的每行数据都会指向下一行，形成链表结构，当遇到 Hash 冲突时，会在桶中进行键值的查找。
2. 特点
* Hash值的大小关系并不一定和Hash运算前的键值完全一样
* Hash索引在计算Hash值的时候是组合索引键合并后再一起计算Hash值，而不是单独计算Hash值
* Hash索引遇到大量Hash值相等的情况后性能并不一定就会比BTree索引高
* Hash 索引指向的数据是无序的，因此无法起到排序优化的作用
### BTree(平衡多路查找树)索引
1. B+Tree数据结构特点
* 关键字数和子树相同
* 非叶子节点仅用作索引，它的关键字和子节点有重复元素
* 叶子节点用指针连在一起

![](https://img-blog.csdn.net/20180529000659117?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEyNDA4Nzc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
### hash和BTree的区别
|  hash   | BTree  |
|  ----  | ----  |
| 仅仅能满足“=”,“IN”,“<=>”查询，不能使用范围查询。  | 支持范围查询 |
| 不能利用组合索引的部分索引键查询  | 支持组合索引的最左匹配原则 |
| 不支持 ORDER BY 排序  | 支持,B+ 树索引数据是有序的 |
| 不支持模糊查询  | 支持|
|等值查询效率更高(列重复值低的情况除外)|先从根节点查起|
## 索引方式
### 聚集索引
聚集索引的叶子节点存储了整个行数据(即:一张表只能有一个聚集索引) innodb。
### 非聚集索引
叶子节点并不包含行记录的全部数据。叶子节点除了包含键值以外，还存储了一个指向改行数据的聚集索引建的书签 。
## 索引类型
* 普通索引  无限制
* 唯一索引 索引列的值必须唯一，但允许有空值,不能作为外键
* 主键索引  一张表只能有一个主键索引,唯一,不允许为空
* 组合索引  最左匹配原则
* 全文索引 fulltext索引配合match ... against操作使用,char、varchar，text 列上支持创建全文索引
## 索引建立原则
* 利用最左前缀：Mysql会一直向右查找直到遇到范围操作（>，<，like、between）就停止匹配。比如a=1 and b=2 and c>3 and d=6；此时如果建立了（a,b,c,d）索引，那么后面的d索引是完全没有用到，当换成了（a,b,d,c）就可以用到。
* 不能过度索引：在修改表内容的时候，索引必须更新或者重构，所以索引过多时，会消耗更多的时间。
* 尽量扩展索引而不要新建索引
* 最适合的索引的列是出现在where子句中的列或连接子句中指定的列。
* 不同值较少的列不必要建立索引（性别）。
# 乐观锁和悲观锁比较
|悲观锁|	乐观锁|
|  ----  | ----  |
|查询时直接锁住记录使得其它事务不能查询，更不能更新|提交更新时检查版本或者时间戳是否符合|
|select ... for update|使用 version 或者 timestamp 进行比较|
|数据库本身|开发者|
|并发量小|并发量大|
|类比Java Synchronized关键字|CAS 算法|

