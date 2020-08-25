# mysql 优化
## 设计
### 存储引擎
### 字段类型
### 范式与逆范式
## 功能
### 索引
### 缓存
### 分区分表
## 架构
### 主从复制
### 读写分离
### 负载均衡

合理SQL：测试，经验。
# 存储引擎
## innodb
## myisam
## 区别
|  innodb   | myisam  |
|  ----  | ----  |
| 支持事务  | 不 |
| 支持行锁,表锁  | 不能 |
|  B+Tree表数据文件和索引文件是分离的，索引文件仅保存数据记录的磁盘地址  |  B+Tree表数据文件本身就是主索引，叶节点data域保存了完整的数据记录 |
# 索引
## 主键索引和唯一索引区别
|  主键索引   | 唯一索引  |
|  ----  | ----  |
| 不能为空  | 能为空 |
| 能作为外键  | 不能 |
| Innodb下查询更快  | Innodb下需要先找到主键索引再找到数据 |

# 悲观锁
## 实现形式
select ... for update
## 注意
查询如果触发索引则只会锁行,否则全表扫描的话会锁表
## 示例
//step1: 查出商品状态
select quantity from items where id=100 for update;
//step2: 根据商品信息生成订单
insert into orders(id,item_id) values(null,100);
//step3: 修改商品的库存
update Items set quantity=quantity-2 where id=100;
