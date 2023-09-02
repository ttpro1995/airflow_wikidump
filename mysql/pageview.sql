CREATE TABLE `pageview` (
  `timestamp` integer,
  `article` varchar(255),
  `views` integer,
  PRIMARY KEY (`timestamp`, `article`)
);
