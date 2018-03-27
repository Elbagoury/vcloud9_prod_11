
Pre-Installation Requirements
---------------------------

- Install the `latest` version of a python dependency module called ``num2words``. Module page:`https://github.com/savoirfairelinux/num2words`. 
  - You can install it using the ``pip3`` command: `pip3 install num2words`
  - If you face any problem during the installation, please send us an email with a screenshot of the error.

- Install the latest version of python dependency module called ``PyPDF2``. 
  - You can install it using the ``pip3`` command: `pip3 install pypdf2` 

- Download and install the latest version of ``wkhtmltopdf``. 
  - We recommend version ``0.12.4 (with patched qt)``


Installation
------------

NOTE: Before you proceed to install this module, please check the `Pre-Installation Requirements` section above.
This Module is a standard Odoo Module. Once you purchase it, please follow the following steps to install it:

- A download link will be given by Odoo once you purchase this module.

- You need to extract the downloaded file into Odoo 'addons' directory where all other modules are kept or you can put it anywhere else depending on your Odoo Configuration

- It may not be necessary to restart Odoo at this stage, but it is highly recommended.

- Enable developer mode/Debug Mode and go to Apps menu. Click on ``Updates Apps list`` for the new module to appear on the list of Apps. 

- Search for `professional_templates` in the Apps list and then  click on ``Install`` button and wait for it to finish

- After that you can go to Setting --> Technical --> Reports --> Report Styles to create your styles and apply to your documents. Please refer to Module ``Description`` page for illustrated configuration example


Configuration
-------------
Please refer to ``Module Description`` for illustrated steps on how to choose one among the multiple templates, colors, fonts, font size, and logos for your reports



Compatibility
------------

- Fully Supports Odoo Version 11.0 Community and Enterprise Editions


Frequently Asked Questions (FAQs)
===========================================

 - How do I print the reports in a different language?

        First you need to translate the templates into your language. Please learn about how to do translation in Odoo here: https://www.odoo.com/documentation/10.0/reference/translations.html

        You can also purchase the module and request for our help (open a ticket by sending email to support@optima.co.ke) on how to translate to a language of your choice.



 - The `Header` content is overlapping the `Body` content of the report?

	
	This is usually caused by the `Logo` or the `Company Address` being too large.

	This is not a big problem since in Odoo you can adjust the Paper Sizes to match the size of your logo or Address.

		- If this happens, Enable `Debug Mode` in Odoo 9.0 in order to access the Extra `Technical Settings` 

		- Go to `Settings -> Technical -> Reports -> Paper Format` and open `European A4` or `US letter` depending on your region or localization

		- Adjust the `Top Margin` and `Header Spacing` until you get an optima size to match the size of your logo or address

                - If you need help just send us a mail to support@optima.co.ke
 
