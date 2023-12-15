
from robocorp.tasks import task
from robocorp import browser
from robocorp.browser import Page

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF

#https://robocorp.com/docs/courses/build-a-robot-python
#Xpath  https://www.simplilearn.com/tutorials/selenium-tutorial/xpath-in-selenium

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    open_robot_order_website()
    close_alert()
    download_Orders_CSV_file()
    fill_the_form()

def open_robot_order_website():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def close_alert():
    page = browser.page()
    page.click("button:text('OK')")

def download_Orders_CSV_file():
    """Downloads CSV file from the given URL"""
    http = HTTP()
    http.download(url=" https://robotsparebinindustries.com/orders.csv", overwrite=True)

def read_orders_csv():
    csv_lib = Tables()
    orders = csv_lib.read_table_from_csv(
    "orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"]
    ) 
    return  orders
    
def fill_the_form():
    orders = read_orders_csv()
    order_id = 0
    for order in orders :
        order_id +=1
        page = browser.page()
        page.select_option("#head", str(order["Head"]))
        page.click("//label[./input[@value="+str(order["Body"])+"]]")
        legs_input_xpath = """//input[@placeholder="Enter the part number for the legs"]"""
        page.fill(legs_input_xpath, order["Legs"])
        page.fill("#address", order["Address"])
        page.click("text=Order")
        page.click("text=Preview")
        #page.click("text=Order another robot")
        #close_alert()
        export_as_pdf("Order_"+str(order_id), page)

def export_as_pdf(order_id:str, page:Page):
    """Export the data to a pdf file"""

    # Capture data table div id and get it as html to the variable
    order_html = page.locator("#root").inner_html()

    pdf = PDF()
    pdf_file = "output/orders/"+order_id+".pdf"
    pdf.html_to_pdf(order_html, pdf_file)
    take_bot_screenshot()
    merge_bot_screenshot_and_order_pdf(pdf_file, pdf, order_id)
    

def take_bot_screenshot():
    """Take a screenshot of the page"""
    #robot-preview-image
    page = browser.page()
    page.locator("#robot-preview-image")
    page.screenshot(path="output/order_bot.png")
    page.screenshot

def merge_bot_screenshot_and_order_pdf(pdf_file:str, pdf:PDF, order_id:str):
    list_of_files = [
        pdf_file,
        'output/order_bot.png',
    ]
    pdf.add_files_to_pdf(
        files=list_of_files,
        target_document="output/Order_Pdf/"+order_id+".pdf"
    )

        

