CREATE TABLE IF NOT EXISTS `ranking`(
  `MusicID` INT(11) NOT NULL DEFAULT '0',
  `Rank` INT(11) NOT NULL DEFAULT '0',
  `Date` DATE NOT NULL DEFAULT '2000-01-01',
  PRIMARY KEY (`MusicID`)
);
