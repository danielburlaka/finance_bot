create table budget(
    codename varchar(255) primary key,
    daily_limit integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_expense, aliases)
values
    ("products", "продукты", true, "еда, хавка, жрачка"),
    ("food", "еда", true, "ресторан, мак, кфс, выпечка"),
    ("transport", "общ. транспорт", false, "метро, автобус, маршрутка"),
    ("taxi", "такси", false, "такс, убер, уклон"),
    ("phone", "телефон", false, "водафон, телеф"),
    ("clothing", "одежда", false, "шмотки"),
    ("internet", "интернет", false, "инет, inet"),
    ("music", "музыка", false, "подписка"),
    ("other", "прочее", false, "");

insert into budget(codename, daily_limit) values ('base', 400);
