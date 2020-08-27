## 基础

### 基本数据类型
Java基本类型占用的字节数：
* 1字节： byte , boolean
* 2字节： short , char
* 4字节： int , float
* 8字节： long , double

编码与中文：
Unicode/GBK： 中文2字节
UTF-8： 中文通常3字节，在拓展B区之后的是4字节
综上，中文字符在编码中占用的字节数一般是2-4个字节。

### 面对对象

#### 1. 理解:

面向对象是向现实世界模型的自然延伸，这是一种”万物皆对象”的编程思想。在现实生活中的任何物体都可以归为一类事物，而每一个个体都是一类事物的实例。 

#### 2. 特征:

##### 封装

将一类事物的属性和行为抽象成一个类，一般是使其属性私有化，行为公开化，提高了数据的隐秘性的同时，使代码模块化。

##### 继承

基于已有的类的定义为基础，构建新的类，已有的类称为父类，新构建的类称为子类，子类能调用父类的非private修饰的成员，同时还可以自己添加一些新的成员，扩充父类，甚至重写父类已有的方法，更其表现符合子类的特征。

##### 多态

方法的重写、重载与动态连接构成多态性。如果说封装和继承是为了使代码重用，那么多态则是为了实现接口重用。多态的一大作用就是为了解耦–为了解除父子类继承的耦合度。如果说继承中父子类的关系式IS-A的关系，那么接口和实现类之之间的关系式HAS-A。简单来说，多态就是允许父类引用(或接口)指向子类(或实现类)对象。很多的设计模式都是基于面向对象的多态性设计的。

### 设计模式

#### 1. 单例模式:

##### 饿汉式

```java
/**
 * 饿汉式单例模式
 * 每个对象在没有使用之前就已经初始化了。这就可能带来潜在的性能问题
 * 如果这个对象很大呢？没有使用这个对象之前，就把它加载到了内存中去是一种巨大的浪费。
 *
 */
public class EagerSingleton {
    private  static  EagerSingleton es =new EagerSingleton();
    private EagerSingleton() {
    }
    public  static  EagerSingleton getSingleton(){
        return es;
    }
}
```



##### 懒汉式



```java
/**
 * 懒汉式
 * 它使用了延迟加载来保证对象在没有使用之前，是不会进行初始化的。
 * 但是，这种写法线程不安全
 * 这是因为在多个线程可能同时运行到第18行，判断ls为null，于是同时进行了初始化。
 * 所以，这是面临的问题是如何使得这个代码线程安全？很简单，在那个方法前面加一个Synchronized就OK了。
 */
public class LazySingleton {
    private static LazySingleton ls = null;
    private LazySingleton() {
    }
    public static LazySingleton getSingleton() {
        if (ls == null) {
            ls = new LazySingleton();
        }
        return ls;
    }
}
```



##### 双重检查锁 的懒汉式

```java
/**
 * 双重检查锁 单例模式(线程安全)
 * 性能问题:同步的代价必然会一定程度的使程序的并发度降低。线程不安全的原因其实是在初始化对象的时候，
 * 可以想办法把同步的粒度降低，只在初始化对象的时候进行同步。这里有必要提出一种新的设计思想——双重检查锁（Double-Checked Lock）。
 */
public final class DoubleCheckedSingleton {
    private static DoubleCheckedSingleton singObj = null;
    private DoubleCheckedSingleton(){
    }
    public static DoubleCheckedSingleton getSingleInstance(){
        if(null == singObj ) {
            synchronized (DoubleCheckedSingleton.class){
                if(null == singObj)
                    singObj = new DoubleCheckedSingleton();
            }
        }
        return singObj;
    }
}
```



##### Initialization on Demand Holder

```java
/**
 * Initialization on Demand Holder  (线程安全,占用资源低)
 * 这种方法使用内部类来做到延迟加载对象，在初始化这个内部类的时候，
 * JLS(Java Language Sepcification)会保证这个类的线程安全。
 * 这种写法最大的美在于，完全使用了Java虚拟机的机制进行同步保证，没有一个同步的关键字。
 */
public class Singleton {
    private static class SingletonHolder {
        final static Singleton instance = new Singleton();
    }
    private Singleton() {
    }
    public static Singleton getInstance() {
        return SingletonHolder.instance;
    }
}

```



### 并发编程

#### 1. 并发编程的三大特性


|  原子性   | 可见性  |有序性  |
|  ----  | ----  |----  |
| 提供互斥访问,同一时刻只能有一个线程对数据进行操作  | 一个线程对主内存的修改，其他线程能够立即看得 |即程序执行的顺序按照代码的先后顺序执行 (happen-before原则)。 |
| Synchronized、Automic工具类、Lock包工具类| Synchronized、volatile、Lock包工具类 |Synchronized、volatile、Lock包工具类 |


#### 2. 线程生命周期

* NEW      线程被创建还没有调用start的时候
* RUNNABLE JVM启动了这个任务
* BLOCKED  进入或重新进入synchronized 代码块或方法被阻塞,没有获取到监视器锁
* WAITING  无限期等待另一个线程执行一个特别的动作.由于Object.wait()、Thread.join()或LockSupport.park() 方法调用,处于的状态,等待被Object.notify()或Object.notifyAll()或LockSupport.unpark()
* TIMED_WAITING 指定时间地等待另一个线程执行一个特别的动作
* TERMINATED 执行完成

![img](file:///C:\Users\sKF8412\AppData\Local\Temp\msohtmlclip1\01\clip_image012.png)

#### 3. 线程方法
|  方法  | 描述 |
|  ----  | ----  |
|  sleep()   |  线程睡眠,释放cpu执行权,不释放锁 |
|  wait()    |   线程等待,释放cpu 执行权,释放锁,只能等待 notify()唤醒|
|  notify()  | 唤醒被wait 的线程 |
|  join()  | 当前线程调用其他线程的join方法，会阻塞当前线程，直到其他线程执行完毕，才会进入就绪状态,释放cpu执行权,释放锁|
|  yield()  | 调用 yield()方法会让当前线程交出CPU资源，让CPU去执行其他的线程。yield()方法只能让 拥有相同优先级的线程 有获取 CPU 执行时间的机会；并不会让线程进入阻塞状态，而是让线程重回就绪状态，它只需要等待重新得到 CPU 的执行；它不释放锁。 |



#### 4. 线程同步

##### Synchronized关键字

```java
   //同步方法
    public synchronized void save(int money) {
        account += money;
    }

    void save1(int money) {
        //同步代码块
        synchronized (this) {
            System.out.println(Thread.currentThread().getName());
            account += money;
        }

    }
```

##### Object 类的wait()和notify()

##### ReentrantLock 重入锁

```java
private Lock lock = new ReentrantLock();

    int getAccount() {
        return account;
    }

    //这里不再需要synchronized
    void save(int money) {
        lock.lock();
        try {
            account += money;
        } finally {
            lock.unlock();
        }

    }
```



##### ThreadLocal 线程变量

使用:

Threadlocal为每个线程提供独立的变量副本,而不会影响其他线程所对应的副本.可以创建多个线程变量

使用场景:

适用于无状态,副本变量独立后不影响业务逻辑的高并发场景. 例如数据库连接管理、线程会话session管理、

RocketMQUtil工具类使用ThreadLocal存放producer和consumer

 

```java
//只改Bank类，其余代码与上同
 class Bank{
    //使用ThreadLocal类管理共享变量account
    private static ThreadLocal<Integer> account = ThreadLocal.withInitial(() -> 100);
    void save(int money){
        account.set(account.get()+money);
        System.out.println("当前线程名称 ==> "+Thread.currentThread().getName());
    }
     int getAccount(){
        return account.get();
    }
}
```



##### LinkedBlockingQueue 阻塞队列

```java
class LinkBlockThread implements Runnable {

    /**
     * 定义一个阻塞队列用来存储生产出来的商品
     */
    private LinkedBlockingQueue<Integer> queue = new LinkedBlockingQueue<>();
    /**
     * 定义生产商品个数
     */
    private static final int size = 10;
    /**
     * 定义启动线程的标志，为0时，启动生产商品的线程；为1时，启动消费商品的线程
     */
    private int flag = 0;

    @Override
    public void run() {
      int new_flag = flag++; //后++ 先赋值再自增
        System.out.println("启动线程 " + new_flag);
        if (new_flag == 0) {
            for (int i = 0; i < size; i++) {
                int b = new Random().nextInt(255);
                System.out.println("生产商品：" + b + "号" + " 线程 ==> " + Thread.currentThread().getName());
                try {
                    queue.put(b);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                System.out.println("仓库中还有商品：" + queue.size() + "个" + " 线程 ==> " + Thread.currentThread().getName());
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        } else {
            for (int i = 0; i < size + 1; i++) {
                try {
                    System.out.println(Thread.currentThread().getState());
                    int n = queue.take();
                    System.out.println("消费者买去了" + n + "号商品" + " 线程 ==> " + Thread.currentThread().getName());
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                System.out.println("仓库中还有商品：" + queue.size() + "个" + " 线程 ==> " + Thread.currentThread().getName());
                try {
                    Thread.sleep(100);
                } catch (Exception e) {
                    // TODO: handle exception
                    e.printStackTrace();
                }
            }
        }
    }
}
```







#### 4. 使用多线程

方法上加@Async(**"asyncServiceExecutor"**) 里面为线程池名称

#### 

#### 5. 线程池

##### 1. 类型

###### 可缓存线程池

Executors.newCacheThreadPool()

可缓存线程池，先查看池中有没有以前建立的线程，如果有，就直接使用。如果没有，就建一个新的线程加入池中，缓存型池子通常用于执行一些生存期很短的异步型任务

###### 固定个数线程池

Executors.newFixedThreadPool(int n)

创建一个可重用固定个数的线程池，以共享的无界队列方式来运行这些线程。

###### 定时任务线程池

Executors.newScheduledThreadPool(int n)

创建一个定长线程池，支持定时及周期性任务执行

###### 单线程化线程池

Executors.newSingleThreadExecutor()

创建一个单线程化的线程池，它只会用唯一的工作线程来执行任务，保证所有任务按照指定顺序(FIFO, LIFO, 优先级)执行。

###### WorkStealing 线程池

Executors.newWorkStealingPool(int parallelism)

构建ForkJoinPool(与其他四个不同),利用Work-Stealing算法，并行地处理任务，不保证处理顺序。 

#####  2. 参数

| 参数名                  |                             含义                             |
| ----------------------- | :----------------------------------------------------------: |
| corePoolSize            | 核心线程数，核心线程会一直存活，即使没有任务需要处理。当线程数小于核心线程数时，即使现有的线程空闲，线程池也会优先创建新线程来处理任务，而不是直接交给现有的线程处理；核心线程在allowCoreThreadTimeout被设置为true时会超时退出，默认情况下不会退出。 |
| maximumPoolSize         | 最大线程数。当线程数大于或等于核心线程，且任务队列已满时，线程池会创建新的线程，直到线程数量达到maxPoolSize。如果线程数等于最大线程数，则已经超出线程池的处理能力，线程池会拒绝处理任务而抛出异常。 |
| keepAliveTime           | 空闲的线程(即在任务队列已满时，又创建的线程)多长时间会被销毁。当线程空闲时间达到keepAliveTime，该线程会退出，直到线程数量达到corePoolSize。如果allowCoreThreadTimeout被设置为true，则所有线程均会退出直到线程数量为0. |
| allowCoreThreadTimeout  |                  是否允许核心线程空闲退出。                  |
| queueCapacity           | 任务队列容量。从maxPoolSize的描述上可以看出，任务队列的容量会影响到线程的变化，因此任务队列的长度也需要恰当的设置。 |
| RejectedExcutionHandler | 饱和策略。当队列和线程池都满了，说明线程池处于饱和状态，那么必须对新提交的任务采用一种特殊的策略来进行处理。这个策略默认配置是AbortPolicy，表示无法处理新的任务而抛出异常。JAVA提供了4中策略**①**。 |
| unit                    | 保持活跃时间的单位。可选为：NANOSECONDS，MICROSECONDS，MILLISECONDS，SECONDS，MINUTES，HOURS，DAYS等。 |
| workQueue               | 工作队列。这队列用来保持那些execute()方法提交的还没有执行的任务。常用的队列SynchronousQueue,LinkedBlockingDeque,ArrayBlockingQueue **②**。一般我们需要根据自己的实际业务需求选择合适的工作队列。 |
| threadFactory           | 线程工厂。当线程池需要创建线程的时候用来创建线程。默认是Executors类的静态内部类DefaultThreadFactory。 |

 

##### 3. 拒绝策略

ThreadPoolExecutor.AbortPolicy:丢弃任务并抛出RejectedExecutionException异常。
ThreadPoolExecutor.DiscardPolicy：也是丢弃任务，但是不抛出异常。
ThreadPoolExecutor.DiscardOldestPolicy：丢弃队列最前面的任务，然后重新尝试执行任务（重复此过程）
ThreadPoolExecutor.CallerRunsPolicy：由调用线程处理该任务

##### 4. 工作队列

SynchronousQueue：直接传递。对于一个好的默认的工作队列选择是SynchronousQueue，该队列传递任务到线程而不持有它们。在这一点上，试图向该队列压入一个任务，如果没有可用的线程立刻运行任务，那么就会入列失败，所以一个新的线程就会被创建。当处理那些内部依赖的任务集合时，这个选择可以避免锁住。直接接传递通常需要无边界的最大线程数来避免新提交任务被拒绝处理。当任务以平均快于被处理的速度提交到线程池时，它依次地确认无边界线程增长的可能性；

LinkedBlockingDeque：无界队列。没有预先定义容量的无界队列，在核心线程数都繁忙的时候会使新提交的任务在队列中等待被执行，所以将不会创建更多的线程，因此，最大线程数的值将不起作用。当每个任务之间是相互独立的时比较适合该队列，所以任务之间不能互相影响执行。例如，在一个WEB页面服务器，当平滑的出现短暂的请求爆发时这个类型的队列是非常有用的，当任务以快于平均处理速度被提交时该队列会确认无边界队列增长的可能性。

ArrayBlockingQueue：有界阻塞队列，遵循FIFO原则，一旦创建容量不能改变，当向一个已经满了的该队列中添加元素和向一个已经为空的该队列取出元素都会导致阻塞；当线程池使用有限的最大线程数时该队列可以帮助保护资源枯竭，但它更难协调和控制。队列大小和最大线程数在性能上可以互相交换：使用大队列和小线程池会降低CPU使用和OS资源与上下文切换开销，但会导致人为降低吞吐量，如果任务频繁阻塞，系统的线程调度时间会超过我们的允许值；如果使用小队列大池，这将会使CPU较为繁忙但会出现难以接受的调度开销，这也会导致降低吞吐量。

## 数据结构

### 基本数据结构

#### 1. 数组

优点:

1、按照索引查询元素速度快 
 2、按照索引遍历数组方便

缺点:

 1、  数组的大小固定后就无法扩容了 
 2、数组只能存储一种类型的数据 
 3、添加，删除的操作慢，因为要移动其他的元素。

### 常用数据结构

#### 1. ArrayList

底层: 数组

第一次添加默认长度 10

扩容机制 1.5倍

每次增加都会使用 Arrays.copyof()创建一个新数组

优点:查询快

缺点:增删慢,线程不安全

#### 2. LinkedList

基于链表实现的列表

适合增删较多的场合

#### 3. TreeSet

基于二叉排序树(红黑树)实现的,

TreeSet最典型的就是它用到了两种排序方式(内部比较器,外部比较器)

#### 4. HashMap

* 底层:数组+链表

* 扩容机制2倍

* 加载因子0.75

* key和value都可以为null

* 线程不安全

* put(k,v)原理:通过key的hash值得到数组下标，然后把entry插到该数组，假如有两个不同的key被分到相同的下标，也就是哈希冲突，那么该数组在该下标下就会形成链表

##### hashmap与hashtable与ConcurrentHashMap区别
|  hashmap   | hashtable  | ConcurrentHashMap|
|  ----  | ----  |----  |
|  继承自AbstractMap类 |  继承自Dictionary类| 继承自AbstractMap类,实现了ConcurrentMap接口 |
| 默认长度16  | 默认长度11 |-|
| 2倍扩容  | 2倍加1扩容 |段内扩容（段内元素超过该段对应Entry数组长度的75%触发扩容，不会对整个Map进行扩容）
|  重新计算hash值 | 直接使用对象的hashCode |直接使用对象的hashCode|
|  线程不安全    | 线程安全,每个方法都有Synchornized修饰 | 线程安全,采用分段锁技术(首先将数据分成一段一段的存储，然后给每一段数据配一把锁，当一个线程占用锁访问其中一个段数据的时候，其他段的数据也能被其他线程访问) |

##### hashmap与hashtable相同点
* 都是hash表实现
* 数组+链表数据结构
* 都是通过单链表解决冲突问题
* 加载因子都为0.75



#### 5. HashSet

实现基于HashMap实现,只不过将value固定为PRESENT

#### 6. LinkedHashMap

支持按照插入顺序排序

#### 7. PriorityQueue

优先级队列,一个基于优先级堆的无界优先级队列

#### 8. CopyOnWriteArraylist

线程安全



 

## 关键字

### final

(1) 被final关键字修饰的类不能被继承

(2) 被final 修饰的基础类型变量的值不能被修改

(3) 被final 修饰的引用类型变量的引用(内存地址)不能被修改,引用指向的对象是可以修改的

 

### transient(被修饰的变量不被序列化)

(1) 变量被transient修饰，变量将不再是对象持久化的一部分，该变量内容在序列化后无法获得访问。

(2) transient关键字只能修饰变量，而不能修饰方法和类。注意，本地变量是不能被transient关键字修饰的。变量如果是用户自定义类变量，则该类需要实现Serializable接口

(3) 被transient关键字修饰的变量不再能被序列化，一个静态变量不管是否被transient修饰，均不能被序列化。

### volatile(保证并发编程中变量的可见性)

一个变量被volatile修饰后，表示着线程本地内存无效，当一个线程修改共享变量后他会立即被更新到主内存中，其他线程读取共享变量时，会直接从主内存中读取

## 集合排序

### 内部比较器

内部比较器就是把比较器定义在实体类的内部，这是要实现的接口为Comparable,重写compareTo,实现包含实体类对象的集合的排序时，调用的是Collections.sort(list).

### 外部比较器

外部比较器，实现Comparator,重写compare。排序时调用的函数是Collections.sort(list,比较器)。

## 反射机制

1.概念

在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法；对于任意一个对象，都能够调用它的任意一个方法和属性；这种动态获取的信息以及动态调用对象的方法的功能称为java语言的反射机制。

2.利用反射机制创建对象

\1.   获取Class对象的三种方式

(1) Class.forName(全限定类名)

(2) Hero.class

(3) new Hero().getClass()

\2. 获取构造器对象

Constructor con = clazz.getConstructor(形参.class);

\3. 获取对象

Hero hero =con.newInstance(实参);

3.使用场景

数据库注册驱动

AOP动态代理



## hashcode()与equals()

(1) 在哈希表中才有用,其他地方没用

(2) 哈希冲突: hashcode() 相等,equals不相等

(3) hashcode()作用: hashCode()的存在主要是用于查找的快捷性

如Hashtable，HashMap等，HashCode经常用于确定对象的存储地址；

(4) equals()作用:hashmap使用equals()判断当前键是否与表中存在的键相同

## String类型的内部实现方式 , 为什么string 不可变

string 内部是用final 修饰的字符数组 ,不可变的是对象, 引用可变

## spring

### AOP实现原理 :动态代理

#### jdk代理

##### 1. 概念

利用反射机制

JDK动态代理只能对实现了接口的类生成代理，而不能针对类

##### 2.  实现

实现InvocationHandler接口

```java
public class JdkProxy implements InvocationHandler {
    private Object target;//需要代理的目标对象

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        Object result = method.invoke(target, args);
        return result;
    }

    //定义获取代理对象方法
    private Object getJDKProxy(Object targetObject) {
        //为目标对象target赋值
        this.target = targetObject;
        //JDK动态代理只能针对实现了接口的类进行代理，newProxyInstance 函数所需参数就可看出
        return Proxy.newProxyInstance(targetObject.getClass().getClassLoader(), targetObject.getClass().getInterfaces(), this);
    }

    public static void main(String[] args) {
        JdkProxy jdkProxy = new JdkProxy();//实例化JDKProxy对象
        UserManagerImpl user = (UserManagerImpl) jdkProxy.getJDKProxy(new UserManagerImpl());//获取代理对象
        user.addUser("admin", "123123");//执行新增方法
    }

}
```



#### cglib动态代理

##### 1. 概念

利用ASM(开源的java字节码编辑库,操作字节码),将代理对象 类的class文件加载出来,通过修改其字节码生成子类来处理

 

用CGlib生成代理类是目标类的子类

##### 2. 实现

实现MethodInterceptor接口

```java
//Cglib动态代理，实现MethodInterceptor接口
public class CglibProxy implements MethodInterceptor {
    private Object target;//需要代理的目标对象
    //重写拦截方法
    @Override
    public Object intercept(Object obj, Method method, Object[] arr, MethodProxy proxy) throws Throwable {
        Object invoke = method.invoke(target, arr);//方法执行，参数：target 目标对象 arr参数数组
        return invoke;
    }
    //定义获取代理对象方法
    private Object getCglibProxy(Object objectTarget){
        //为目标对象target赋值
        this.target = objectTarget;
        Enhancer enhancer = new Enhancer();
        //设置父类,因为Cglib是针对指定的类生成一个子类，所以需要指定父类
        enhancer.setSuperclass(objectTarget.getClass());
        enhancer.setCallback(this);// 设置回调
        return enhancer.create();
    }
    public static void main(String[] args) {
        CglibProxy cglib = new CglibProxy();//实例化CglibProxy对象
        UserCglibTest cglibProxy = (UserCglibTest)cglib.getCglibProxy(new UserCglibTest());
        cglibProxy.addUser("asd","123");
    }
}
```

