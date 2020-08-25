# 存储引擎
## innodb
## myisam

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
