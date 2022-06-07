CREATE TABLE `item` (
  `id` INT PRIMARY KEY NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `big_class` VARCHAR(20) NOT NULL,
  `mid_class` VARCHAR(20) NOT NULL,
  `brand` VARCHAR(100) NOT NULL,
  `serial_number` VARCHAR(100) NOT NULL,
  `gender` VARCHAR(10) NOT NULL,
  `season` VARCHAR(20),
  `cum_sale` INT,
  `view_count` decimal(8,1),
  `likes` INT NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  `price` INT NOT NULL,
  `R` INT NOT NULL,
  `G` INT NOT NULL,
  `B` INT NOT NULL,
  `color_id` INT NOT NULL,
  `season_year` decimal(5,1),
  `most_bought_age_class` INT NOT NULL,
  `men_bought_ratio` INT NOT NULL,
  `cluster_id` INT NOT NULL,
  `img_url` VARCHAR(100) NOT NULL,
  `url` VARCHAR(100) NOT NULL
);

CREATE TABLE `item_fit` (
  `id` INT NOT NULL,
  `fit` VARCHAR(20) NOT NULL,
  UNIQUE(id, fit),
  FOREIGN KEY(id) REFERENCES item(id)
);

CREATE TABLE `item_four_season` (
  `id` INT NOT NULL,
  `four_season` VARCHAR(10) NOT NULL,
  UNIQUE(id, four_season),
  FOREIGN KEY(id) REFERENCES item(id)
);

CREATE TABLE `item_tag` (
  `id` INT NOT NULL,
  `tag` VARCHAR(100) NOT NULL,
  UNIQUE(id, tag),
  FOREIGN KEY(id) REFERENCES item(id)
);

CREATE TABLE `item_rel_codi_url` (
  `id` INT NOT NULL,
  `rel_codi_url` VARCHAR(100) NOT NULL,
  UNIQUE(id, rel_codi_url),
  FOREIGN KEY(id) REFERENCES item(id)
);

CREATE TABLE `item_buy_gender` (
  `id` INT PRIMARY KEY NOT NULL,
  `buy_men` INT NOT NULL,
  `buy_women` INT NOT NULL,
  FOREIGN KEY(id) REFERENCES item(id)
);

CREATE TABLE `item_buy_age` (
  `id` INT PRIMARY KEY NOT NULL,
  `buy_age_18` INT NOT NULL,
  `buy_age_19_23` INT NOT NULL,
  `buy_age_24_28` INT NOT NULL,
  `buy_age_29_33` INT NOT NULL,
  `buy_age_34_39` INT NOT NULL,
  `buy_age_40` INT NOT NULL,
  FOREIGN KEY(id) REFERENCES item(id)
);

CREATE TABLE `item_codi_id` (
  `id` INT NOT NULL,
  `codi_id` INT NOT NULL,
  UNIQUE(id, codi_id),
  FOREIGN KEY(id) REFERENCES item(id),
  FOREIGN KEY(codi_id) REFERENCES codi(id)
);

CREATE TABLE `codi` (
  `id` INT PRIMARY KEY NOT NULL,
  `style` VARCHAR(30),
  `img_url` VARCHAR(100) NOT NULL,
  `url` VARCHAR(100) NOT NULL,
  `popularity` INT NOT NULL
);

CREATE TABLE `codi_tag` (
  `id` INT NOT NULL,
  `tag` VARCHAR(100),
  FOREIGN KEY(id) REFERENCES codi(id)
);