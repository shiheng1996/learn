# spring aop
利用动态代理实现

## jdk动态代理
利用反射机制,只能对实现了InvocationHandler接口的类生成代理
## cglib动态代理
利用ASM(开源的java字节码编辑库,操作字节码),将代理对象 类的class文件加载出来,通过修改其字节码生成子类来处理
用CGlib生成代理类是目标类的子类
## 区别
|  jdk代理   | cglib代理  |
|  ----  | ----  |
| 可以  | 不能对声明为final的方法进行代理 |
| 只能对实现了接口的类生成代理，而不能针对类  | 可以 |
|适用频繁、反复地创建代理对象的场景|不需要频繁创建代理对象的应用，如Spring中默认的单例bean，只需要在容器启动时生成一次代理对象|

# spring bean
## spring bane的生命周期
![](https://img-blog.csdnimg.cn/20200522090616885.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjExNjU1OQ==,size_16,color_FFFFFF,t_70)
1. 
BeanNameAware.setBeanName() 在创建此bean的bean工厂中设置bean的名称，在普通属性设置之后调用，在InitializinngBean.afterPropertiesSet()方法之前调用

BeanClassLoaderAware.setBeanClassLoader(): 在普通属性设置之后，InitializingBean.afterPropertiesSet()之前调用

BeanFactoryAware.setBeanFactory() : 回调提供了自己的bean实例工厂，在普通属性设置之后，在InitializingBean.afterPropertiesSet()或者自定义初始化方法之前调用

EnvironmentAware.setEnvironment(): 设置environment在组件使用时调用

EmbeddedValueResolverAware.setEmbeddedValueResolver(): 设置StringValueResolver 用来解决嵌入式的值域问题

ResourceLoaderAware.setResourceLoader(): 在普通bean对象之后调用，在afterPropertiesSet 或者自定义的init-method 之前调用，在 ApplicationContextAware 之前调用。

ApplicationEventPublisherAware.setApplicationEventPublisher(): 在普通bean属性之后调用，在初始化调用afterPropertiesSet 或者自定义初始化方法之前调用。在 ApplicationContextAware 之前调用。

MessageSourceAware.setMessageSource(): 在普通bean属性之后调用，在初始化调用afterPropertiesSet 或者自定义初始化方法之前调用，在 ApplicationContextAware 之前调用。

ApplicationContextAware.setApplicationContext(): 在普通Bean对象生成之后调用，在InitializingBean.afterPropertiesSet之前调用或者用户自定义初始化方法之前。在ResourceLoaderAware.setResourceLoader，ApplicationEventPublisherAware.setApplicationEventPublisher，MessageSourceAware之后调用。

ServletContextAware.setServletContext(): 运行时设置ServletContext，在普通bean初始化后调用，在InitializingBean.afterPropertiesSet之前调用，在 ApplicationContextAware 之后调用注：是在WebApplicationContext 运行时

BeanPostProcessor.postProcessBeforeInitialization() : 将此BeanPostProcessor 应用于给定的新bean实例 在任何bean初始化回调方法(像是InitializingBean.afterPropertiesSet或者自定义的初始化方法）之前调用。这个bean将要准备填充属性的值。返回的bean示例可能被普通对象包装，默认实现返回是一个bean。

BeanPostProcessor.postProcessAfterInitialization() : 将此BeanPostProcessor 应用于给定的新bean实例 在任何bean初始化回调方法(像是InitializingBean.afterPropertiesSet或者自定义的初始化方法)之后调用。这个bean将要准备填充属性的值。返回的bean示例可能被普通对象包装

InitializingBean.afterPropertiesSet(): 被BeanFactory在设置所有bean属性之后调用(并且满足BeanFactory 和 ApplicationContextAware)。

## spring bean 注入循环依赖问题(spring 三级缓存解决set注入和属性注入,构造器注入不能解决)

Spring解决循环依赖的诀窍就在于singletonFactories这个cache，这个cache中存的是类型为ObjectFactory

```Java
/** Cache of singleton objects: bean name --> bean instance */
private final Map<String, Object> singletonObjects = new ConcurrentHashMap<String, Object>(256);  一级缓存
/** Cache of early singleton objects: bean name --> bean instance */
private final Map<String, Object> earlySingletonObjects = new HashMap<String, Object>(16); 二级缓存
/** Cache of singleton factories: bean name --> ObjectFactory */
private final Map<String, ObjectFactory<?>> singletonFactories = new HashMap<String, ObjectFactory<?>>(16);三级缓存

protected Object getSingleton(String beanName, boolean allowEarlyReference) {
   Object singletonObject = this.singletonObjects.get(beanName);
   if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
      synchronized (this.singletonObjects) {
         singletonObject = this.earlySingletonObjects.get(beanName);
         if (singletonObject == null && allowEarlyReference) {
            ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
            if (singletonFactory != null) {
               singletonObject = singletonFactory.getObject();
               this.earlySingletonObjects.put(beanName, singletonObject);
               this.singletonFactories.remove(beanName);
            }
         }
      }
   }
   return (singletonObject != NULL_OBJECT ? singletonObject : null);} 
 ```
Spring首先从singletonObjects（一级缓存）中尝试获取，如果获取不到并且对象在创建中，则尝试从earlySingletonObjects(二级缓存)中获取，如果还是获取不到并且允许从singletonFactories通过getObject获取，则通过singletonFactory.getObject()(三级缓存)获取。如果获取到了则移除对应的singletonFactory,将singletonObject放入到earlySingletonObjects，其实就是将三级缓存提升到二级缓存中！

# SpringBoot
## 核心注解
* @SpringBootApplication 用于Spring主类上最最最核心的注解，自动化配置文件，表示这是一个SpringBoot项目，用于开启SpringBoot的各项能力。@SpringBootConfigryation @EnableAutoConfiguration、@ComponentScan三个注解的组合。
* @EnableAutoConfiguration 允许SpringBoot自动配置注解，开启这个注解之后，SpringBoot就能根据当前类路径下的包或者类来配置Spring Bean。
* @Configuration Spring 3.0添加的一个注解，用来代替applicationContext.xml配置文件，所有这个配置文件里面能做到的事情都可以通过这个注解所在的类来进行注册。
* @ComponentScan Spring 3.1添加的一个注解，用来代替配置文件中的component-scan配置，开启组件扫描，自动扫描包路径下的@Component注解进行注册bean实例放到context(容器)中。
## 跨域
@CrossOrigin 

# SpringSecurity优缺点
# SpringSecurity执行流程
![](https://blog.csdn.net/u012702547/article/details/89629415)



# SpringMVC
## 工作流程
![](https://img2018.cnblogs.com/blog/1121080/201905/1121080-20190509202147059-745656946.jpg)
1. 用户向服务端发送一次请求，这个请求会先到前端控制器DispatcherServlet(也叫中央控制器)。
2. DispatcherServlet接收到请求后会调用HandlerMapping处理器映射器。由此得知，该请求该由哪个Controller来处理（并未调用Controller，只是得知）
3. DispatcherServlet调用HandlerAdapter处理器适配器，告诉处理器适配器应该要去执行哪个Controller
4. HandlerAdapter处理器适配器去执行Controller并得到ModelAndView(数据和视图)，并层层返回给DispatcherServlet
5. DispatcherServlet将ModelAndView交给ViewReslover视图解析器解析，然后返回真正的视图。
6. DispatcherServlet将模型数据填充到视图中
7. DispatcherServlet将结果响应给用户
## 组件
* DispatcherServlet：前端控制器，也称为中央控制器，它是整个请求响应的控制中心，组件的调用由它统一调度。
* HandlerMapping：处理器映射器，它根据用户访问的 URL 映射到对应的后端处理器 Handler。也就是说它知道处理用户请求的后端处理器，但是它并不执行后端处理器，而是将处理器告诉给中央处理器。
* HandlerAdapter：处理器适配器，它调用后端处理器中的方法，返回逻辑视图 ModelAndView 对象。
* ViewResolver：视图解析器，将 ModelAndView 逻辑视图解析为具体的视图（如 JSP）。
* Handler：后端处理器，对用户具体请求进行处理，也就是我们编写的 Controller 类。

