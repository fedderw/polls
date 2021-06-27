CREATE TABLE `polls` (
  `poll_id` int unsigned NOT NULL,
  `date` date NOT NULL,
  `pollster` varchar(255) NOT NULL,
  `sample_size` int unsigned NOT NULL,
  `margin_of_error` varchar(255),
  `demographic` varchar(255),
  `country` varchar(255) NOT NULL,
  `crosstabs_entered` varchar(255),
  `crosstabs_not_entered` varchar(255),
  `is_complete` bit(1) NOT NULL,
  `If incomplete, emailed?` varchar(255),
  `Link` varchar(255) NOT NULL,
  `Notes` longtext,
  PRIMARY KEY (`poll_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `responses` (
  `poll_id` int unsigned NOT NULL,
  `question_id` int unsigned NOT NULL,
  `response` varchar(255) NOT NULL,
  `xtab_var1` varchar(255) NOT NULL,
  `xtab_val1` float NOT NULL,
  `xtab_var2` varchar(255) NOT NULL,
  `xtab_val2` float NOT NULL,
  `percentage` float NOT NULL,
  `notes` longtext,
  PRIMARY KEY (`poll_id`,`question_id`,`response`,`xtab_var1`,`xtab_var2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `pollsters` (
  `pollster` varchar(255) NOT NULL,
  `538 rating` varchar(255) NOT NULL,
  PRIMARY KEY (`pollster`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `questions` (
  `question_id` int unsigned NOT NULL,
  `question_text` varchar(255) NOT NULL,
  `response_scale` longtext,
  PRIMARY KEY (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `regions` (
  `region` varchar(255) NOT NULL,
  `macro_region` varchar(255),
  `Population` int unsigned,
  PRIMARY KEY (`region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `response_favorability` (
  `response` varchar(255) NOT NULL,
  `favorability` tinyint NOT NULL,
  PRIMARY KEY (`response`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- this worked
ALTER TABLE `responses` ADD FOREIGN KEY (`question_id`) REFERENCES `questions` (`question_id`);
-- query error: TEXT/BLOB are not valid types for foreign keys
ALTER TABLE `polls` ADD FOREIGN KEY (`pollster`) REFERENCES `pollsters` (`pollster`);
-- query error: TEXT/BLOB are not valid types for foreign keys
ALTER TABLE `responses` ADD FOREIGN KEY (`response`) REFERENCES `response_favorability` (`response`);
-- this didn't work
ALTER TABLE `polls` ADD FOREIGN KEY (`poll_id`) REFERENCES `responses` (`poll_id`);

/*
run this in the shell:
cmd /c 'dolt sql < C:\Users\fedde\UBICenter\polls\data\sql\schema.sql'
*/

