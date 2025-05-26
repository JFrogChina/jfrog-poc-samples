package org.gradle.api;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

// Remove import for java.util.logging.Logger or LogManager

public class PersonList {

    private static final Logger logger = LogManager.getLogger(PersonList.class);

    public void someMethod() {
        logger.info("This is an info message from Log4j.");
        logger.error("This is an error message from Log4j.");
    }

    // your other methods...
}
