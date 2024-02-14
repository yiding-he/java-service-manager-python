对 SpringBoot 项目做简单打包，连同依赖库一起拷贝到 lib 目录中。执行命令：
java -Dlog.root=./logs -cp ./config;./lib/*; org.example.springboot.SampleApplication --spring.profiles.active=test
