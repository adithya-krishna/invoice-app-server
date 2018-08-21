DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE `invoices` (
	`invoice_id` VARCHAR(10) NOT NULL PRIMARY KEY,
	`tax` TEXT,
	`discount` TEXT,
	`tax_amount` TEXT,
	`discount_amount` TEXT,
	`grand_total` TEXT,
	`sub_total` TEXT
);

CREATE TABLE `customers` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`invoice_id`	TEXT,
	`full_name`	TEXT,
	`address`	TEXT,
	`pincode`	TEXT,
	`phone`	TEXT,
	`email`	TEXT,
	FOREIGN KEY(`invoice_id`) REFERENCES `invoices`(`invoice_id`)
);

CREATE TABLE `products` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`invoice_id`	TEXT,
	`item_name`	TEXT,
	`quantity`	TEXT,
	`value`	TEXT,
	`formatted_quantity`	TEXT,
	`formatted_value`	TEXT,
	FOREIGN KEY(`invoice_id`) REFERENCES `invoices`(`invoice_id`)
);