from . import app,db,cors
from flask import request, Response, jsonify;
from flask.ext.cors import CORS, cross_origin
from .constants import JSON_MIME_TYPE
import json


@app.route('/all-invoices')
@cross_origin(origin='localhost', headers=['Content-Type'])
def get_all_invoices():
	query = ('SELECT i.invoice_id, tax, discount, tax_amount, discount_amount, grand_total, sub_total,'
		' full_name, address, pincode, phone, email, '
		' item_name, quantity, value, formatted_quantity, formatted_value FROM products p '
		' JOIN'
		' invoices i ON i.invoice_id = p.invoice_id'
		' JOIN'
		' customers c ON i.invoice_id = c.invoice_id')

	result = db.db_select(query)
	listOfProducts = []

	entries = {};

	for row in result:
		invoice_id = row[0];
		tax = row[1];
		discount = row[2];
		tax_amount = row[3];
		discount_amount = row[4];
		grand_total = row[5];
		sub_total = row[6];
		full_name = row[7];
		address = row[8];
		pincode = row[9];
		phone = row[10];
		email = row[11];
		item_name = row[12];
		quantity = row[13];
		value = row[14];
		formatted_quantity = row[15];
		formatted_value = row[16];

		if invoice_id not in entries:
			entry = {};
			entry['invoiceID'] = invoice_id;
			entry['tax'] = tax;
			entry['discount'] = discount;
			entry['taxAmount'] = tax_amount;
			entry['discountAmount'] = discount_amount;
			entry['grandTotal'] = grand_total;
			entry['subTotal'] = sub_total;

			customer = {};
			customer['name'] = full_name;
			customer['address'] = address;
			customer['pincode'] = pincode;
			customer['email'] = email;
			customer['phone'] = phone;
			entry['customer'] = customer;

			entry['products'] = [];
			product = {};
			product['quantity'] = quantity;
			product['value'] = value;
			product['formattedValue'] = formatted_value;
			product['formattedQuantity'] = formatted_quantity;
			product['itemName'] = item_name;
			entry['products'].append(product);

			entries[invoice_id] = entry;
		else: 
			product = {};
			product['quantity'] = quantity;
			product['value'] = value;
			product['itemName'] = item_name;
			product['formattedValue'] = formatted_value;
			product['formattedQuantity'] = formatted_quantity;
			entries[invoice_id]['products'].append(product)

	resp = jsonify(entries)
	resp.status_code = 200
	return resp;

@app.route('/save-invoice', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type'])
def save_invoice():
	try:
		data = request.json;
		# save invoice
		invoice = {};
		invoice['invoice_id'] = data['invoiceID'];
		invoice['grand_total'] = data['grandTotal'];
		invoice['sub_total'] = data['subTotal'];
		invoice['tax'] = data['tax'];
		invoice['discount'] = data['discount'];
		invoice['tax_amount'] = data['taxAmount'];
		invoice['discount_amount'] = data['discountAmount'];

		invoiceQuery = """INSERT INTO invoices (invoice_id, grand_total, sub_total, tax, discount, tax_amount, discount_amount) 
				VALUES (:invoice_id, :grand_total, :sub_total, :tax, :discount, :tax_amount, :discount_amount)""";
		result=db.db_execute(invoiceQuery, invoice);

		# save customer
		customer = {};
		customer['invoice_id'] = data['invoiceID'];
		customer['full_name'] = data['customer']['name'];
		customer['phone'] = data['customer']['phone'];
		customer['address'] = data['customer']['address'];
		customer['email'] = data['customer']['email'];
		customer['pincode'] = data['customer']['pincode'];

		customerQuery = """INSERT INTO customers (invoice_id, full_name, phone, address, email, pincode) 
				VALUES (:invoice_id, :full_name, :phone, :address, :email, :pincode);"""
		result=db.db_execute(customerQuery, customer);


		# save products
		for product in data['products']:
			productQuery = """INSERT INTO products (invoice_id, item_name, quantity, value, formatted_quantity, formatted_value) 
				VALUES (:invoice_id, :item_name, :quantity, :value, :formatted_quantity, :formatted_value)"""
			params = {
				'invoice_id': data['invoiceID'],
				'item_name': product['itemName'],
				'quantity': product['quantity'],
				'value': product['value'],
				'formatted_quantity': product['formattedQuantity'],
				'formatted_value': product['formattedValue']
			}
			result=db.db_execute(productQuery, params);

		resp = jsonify({ 'msg': 'successfully saved', 'data': data })
		resp.status_code = 201
		return resp;
	except Exception as ex:
		resp=jsonify({"msg": str(ex), "status":"Failed" })
		resp.status_code = 400
		return resp;
