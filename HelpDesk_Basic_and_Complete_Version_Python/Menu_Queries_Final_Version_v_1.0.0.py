#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 08:42:32 2022

@Author:     alessioborgi
@Contact :   alessioborgi3@gmail.com

@Filename:   Menu_Queries.py
"""
import psycopg2
import psycopg2.extras
import pandas as pd
import getpass

hostname = 'localhost'
database = 'HelpDesk'
username = 'postgres'
pwd = 'admin'
port_id = 5432
conn = None



        



#----------------------------------------------------------------------LEADERSHIP------------------------------------------------------------------------------------------------

menu_options_lead = {            
                            1: '-------------------Select the total number of Closed and Opened Tickets. In addition to this, display the percentantage of Total Ticket over Closed Ticket at this moment.',
                            2: '-------------------Select the Difference in how much HelpDesk gains (sum of external companies contract amount minus how much spend at year (sum of salaries + bonuses). Technically, it is called the                            “Operating Profit”',
                            3: '-------------------Select the Sum of the Salary, The sum of Bonuses, the Sum of Employee, and the Average Annual Salary depending on their Employee_Type(Workforce, Leadership and CEO).',
                            4: '-------------------Select the ID, the Employee Typology, the Name and Surname and their annual salary of the Employees present in the DB. Then select the TOP 10 by taking into account the Annual Salary as                      method of judgement.',
                            5: '-------------------Select the Average number of Certification that HelpDesk’s Employee have got during the year, depending on their type.',
                            6: '-------------------Select the Average Annual Salary of HelpDesk’s Employees have got depending on their Category.',
                            7: '-------------------Select the ID_Employee, its ID_Contract, its Annual and Monthly Salary, and the model and Rent_Price of its car of an employee that have some Stocks of the Company. Moreover, its car                         must have more than 200 Horsepower and less than 200000 kilometers traveled. He must also have a Credit Card included in the Contract.',
                            8: '-------------------Select the Number of Employee’s Cars for every Fleet Company, the sum of the rent price per  Fleet Company, its Id, Name and Address. Return only thosse Fleet Company that have more than                     5 cars rented to HelpDesk’s Employees. ',
                            
                            'Tech1:': '--------------Enter 1_st_Level_Technician Working Area.',
                            'Tech2:': '--------------Enter 2_nd_Level_Technician Working Area.',
                            'HR:': '-----------------Enter Human Resources Working Area.',
                            'Account Manager:': '----Enter Account Manager Working Area.',
                            'Business Manager:': '---Enter Business Manager Working Area.',
                            'Finance:': '------------Enter Finance Working Area.',
                            
                            
                            'Q:': 'Exit',
                            'H:': 'Help', 
                            'B:': 'Back',
                            'L:': 'Go Back to LEADESHIP Working Area (WARNING: Only if you have PERMISSIONS!!!) '
                }

def print_menu_lead():
    print('\n \n\nWELCOME TO THE HELPDESK BASIC APPLICATION v_0.1\n')
    print('LEADERSHIP WORKING AREA: \n')
    for key in menu_options_lead.keys():
        print (key, menu_options_lead[key] )

def Query1_Lead():
    print('RESULT OF THE LEADERSHIP QUERY 1: ')
    Query1_info_Lead()
    
    cur.execute('SELECT t."Total_Tickets", c."Closed_Tickets", o."Open_Tickets", ROUND(CAST((c."Closed_Tickets" * 100.0 / t."Total_Tickets") AS FLOAT)) as "%Closed", ROUND(CAST((o."Open_Tickets"* 100.0 / t."Total_Tickets") AS FLOAT))as "%Opened" \
                 FROM \
                        (SELECT COUNT(*) as "Total_Tickets" \
	  	         FROM "TICKET") as t, \
	 	        \
                        (SELECT COUNT(*)as "Closed_Tickets"\
	  	         FROM "TICKET"  \
	  	         WHERE "Closed_Ticket" = true) as c, \
	 	        \
                        (SELECT COUNT(*)as "Open_Tickets"\
	  	         FROM "TICKET"  \
	  	         WHERE "Closed_Ticket" = false) as o')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Total_Tickets', 'Closed_Tickets', "Open_Tickets", "%Closed", "%Opened"  ]
    print(df)

def Query1_info_Lead():
    print('TASK: Select the total number of Closed and Opened Tickets. In addition to this, display the percentantage of Total Ticket over Closed Ticket at this moment. \n')
 
def Query2_Lead():
    print('RESULT OF THE LEADERSHIP QUERY 8: ')
    Query2_info_Lead()
    cur.execute('SELECT (e."Total_Income")-(s."Total_Salary_Expense" + b."Total_Bonus_Expense"+ car."Total_Car_Expense"+ book."Total_Book_Expense"+ course."Total_Course_Expense"+food."Total_Food_Expense"+credit."Total_Credit_Card_Expense") as "Operating_Profit",\
                 e."Total_Income", s."Total_Salary_Expense", b."Total_Bonus_Expense", car."Total_Car_Expense", book."Total_Book_Expense", course."Total_Course_Expense", food."Total_Food_Expense", credit."Total_Credit_Card_Expense"\
                FROM\
	        (SELECT SUM("Bonus") as "Total_Bonus_Expense"\
	         FROM "CONTRACT"\
                 WHERE "Contract_Expiration" > (SELECT CURRENT_DATE) or "Contract_Expiration" ISNULL) as b,\
                                \
                (SELECT SUM("Salary") as "Total_Salary_Expense"\
                FROM "CONTRACT"\
                WHERE "Contract_Expiration" > (SELECT CURRENT_DATE) or "Contract_Expiration" ISNULL) as s,\
                                \
                (SELECT SUM("Amount_Contract") as "Total_Income"\
                FROM "EXTERNAL_CONTRACT"\
                WHERE "Validity_Contract" > (SELECT CURRENT_DATE) or "Validity_Contract" ISNULL) as e,\
                                \
                (SELECT (SUM("Rent_Price_Car")*12) as "Total_Car_Expense"\
                FROM "CAR_BENEFIT"\
                WHERE "Assigned_Up_To_Car" > (SELECT CURRENT_DATE) or "Assigned_Up_To_Car" ISNULL) as car,\
                                \
                (SELECT SUM("Value_Book_Bonus") as "Total_Book_Expense"\
                FROM "BOOK_BONUS"\
                WHERE "Expiry_Date_Book_Bonus" > (SELECT CURRENT_DATE) or "Expiry_Date_Book_Bonus" ISNULL) as book,\
                                \
                (SELECT SUM("Value_Courses_Bonus") as "Total_Course_Expense"\
                FROM "COURSES_BONUS"\
                WHERE "Expiry_Date_Bonus" > (SELECT CURRENT_DATE) or "Expiry_Date_Bonus" ISNULL) as course,\
                                \
                (SELECT SUM("Value_Food_Stamp") as "Total_Food_Expense"\
                FROM "FOOD_STAMP"\
                WHERE "Expiry_Date_Food_Stamp" > (SELECT CURRENT_DATE) or "Expiry_Date_Food_Stamp" ISNULL) as food,\
                                \
                (SELECT SUM("Current_Expense") as "Total_Credit_Card_Expense"\
                FROM "CREDIT_CARD"\
                WHERE "Expiry_Date_Credit_Card" > (SELECT CURRENT_DATE) or "Expiry_Date_Credit_Card" ISNULL) as credit')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Operating_Profit', 'Total_Income', "Total_Salary_Expense", "Total_Bonus_Expense", "Total_Car_Expense", "Total_Book_Expense", "Total_Course_Expense", "Total_Food_Expense", "Total_Credit_Card_Expense"]
    print(df)

def Query2_info_Lead():
    print('TASK: Select the Difference in how much HelpDesk gains (sum of external companies contract amount minus how much spend at year (sum of salaries + bonuses). Technically, it is called the “Operating Profit”')

   
def Query3_Lead():
    print('RESULT OF THE LEADERSHIP QUERY 3: ')
    Query3_info_Lead()
    
    cur.execute('SELECT (SUM(co."Salary"))*14 as "Sum_Salary", SUM(co."Bonus") as "Sum_Bonus", COUNT(*) as "Number_Employee", "Employee_Type", ROUND(AVG("Salary")*14) as "Average_Salary_Type_Employee_at_Year", ROUND(AVG("Salary")) as "Average_Salary_Type_Employee_at_Month" \
                 FROM "EMPLOYEE" e JOIN "CONTRACT" co ON e."ID_Employee" = co."ID_Employee" \
                 GROUP BY e."Employee_Type" \
                 ORDER BY ROUND(AVG("Salary")) DESC')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Sum_Salary', 'Sum_Bonus', "Number_Employee", "Employee_Type", "Average_Salary_Type_Employee_at_Year", "Average_Salary_Type_Employee_at_Month"  ]
    print(df)

def Query3_info_Lead():
    print('TASK: Select the Sum of the Salary, The sum of Bonuses, the Sum of Employee, and the Average Annual Salary depending on their Employee_Type(Workforce, Leadership and CEO). \n')
    
def Query4_Lead():
    print('RESULT OF THE LEADERSHIP QUERY 4: ')
    Query4_info_Lead()
    
    cur.execute('SELECT e."ID_Employee", e."Employee_Type", e."Name_Employee", e."Surname_Employee", co."Salary"*14  \
                 FROM "EMPLOYEE" e JOIN "CONTRACT" co ON e."ID_Employee" = co."ID_Employee" \
                 ORDER BY co."Salary" DESC\
                 LIMIT 10')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'Employee_Type', "Name_Employee", "Surname_Employee", "Salary"]
    print(df)

def Query4_info_Lead():
    print('TASK: Select the ID, the Employee Typology, the Name and Surname and their annual salary of the Employees present in the DB. Then select the TOP 10 by taking into account the Annual Salary as method of judgement.\n')
    
def Query5_Lead():
    print('RESULT OF THE LEADERSHIP QUERY 5: ')
    Query5_info_Lead()
    
    string = 'SELECT cert."Number_Certification_Tot", cert."Employee_Type", tot."Tot_Employee",ROUND((cert."Number_Certification_Tot"/tot."Tot_Employee")*100.) as "%Certification_per_Employee", y."Number_Certification_Year" as "Number_Certification_Year",ROUND((y."Number_Certification_Year"/tot."Tot_Employee")*100.) as "%Certification_per_Employee_this_Year" \
                 FROM   (\
		         SELECT COUNT(*) as "Number_Certification_Tot", e."Employee_Type"\
                         FROM "EMPLOYEE" e JOIN "ACHIEVEMENT_CERTIFICATION" as ac ON e."ID_Employee" = ac."ID_Employee" JOIN "CERTIFICATION" as ce ON ac."ID_Certification"= ce."ID_Certification"\
    		         GROUP BY e."Employee_Type" \
	   	        ) as cert\
	   	        JOIN \
	   	        (\
                         SELECT COUNT(*) as "Tot_Employee", "Employee_Type" as "Type_Tot_Employee"\
	 	         FROM "EMPLOYEE"\
	     	         GROUP BY "Employee_Type"\
	   	        ) as tot\
	   	        ON cert."Employee_Type"= tot."Type_Tot_Employee"\
	   	        JOIN\
	   	        (\
		         SELECT COUNT(*) as "Number_Certification_Year", e."Employee_Type"\
                         FROM "EMPLOYEE" e JOIN "ACHIEVEMENT_CERTIFICATION" as ac ON e."ID_Employee" = ac."ID_Employee" JOIN "CERTIFICATION" as ce ON ac."ID_Certification"= ce."ID_Certification"\
    		         WHERE "Date_Time_Certification" > current_date - interval ' + "'1 year'" +'\
		         GROUP BY e."Employee_Type" \
	   	        ) as y\
	   	        ON cert."Employee_Type"= y."Employee_Type"'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Number_Certification_Tot', 'Employee_Type', "Tot_Employee", "%Certification_per_Employee", "Number_Certification_Year", "%Certification_per_Employee_this_Year"]
    print(df)

def Query5_info_Lead():
    print('TASK: Select the Average number of Certification that HelpDesk’s Employee have got during the year, depending on their type.')

def Query6_Lead():
    print('RESULT OF THE LEADERSHIP QUERY 6: ')
    Query6_info_Lead()
    string = 'SELECT ceo."Annual_Salary_CEO", l."Annual_Salary_Leadership", tech1."Annual_Salary_1_st_Tech", tech2."Annual_Salary_2_nd_Tech", hr."Annual_Salary_Human_Resources", f."Annual_Salary_Finance", am."Annual_Salary_Account_Manager", bm."Annual_Salary_Business_Manager"\
                 FROM \
                        (SELECT ROUND(AVG(c."Salary")*14) as "Annual_Salary_CEO", ROUND(AVG(c."Bonus")) as "Annual_Bonus_CEO"\
                         FROM "EMPLOYEE" e JOIN "CONTRACT" c ON e."ID_Employee" = c."ID_Employee" \
	                 WHERE e."Employee_Type" = ' + "'CEO'" + ') as ceo,\
                                                \
                                (SELECT ROUND(AVG(c."Salary")*14) as "Annual_Salary_Leadership"\
                                 FROM "EMPLOYEE" e JOIN "CONTRACT" c ON e."ID_Employee" = c."ID_Employee" \
	                         WHERE e."Employee_Type" = ' + "'Leadership'" + ') as l, \
                                                \
                                (SELECT ROUND(AVG(c."Salary")*14) as "Annual_Salary_1_st_Tech"\
                                 FROM "EMPLOYEE" e JOIN "CONTRACT" c ON e."ID_Employee" = c."ID_Employee" \
                                 WHERE e."Employee_Type" = '+ "'Workforce'" + ' and CAST(("e"."ID_Employee").id_role as varchar) LIKE ' + "'IDWT1'"+ ') as tech1,\
                                                \
                                (SELECT ROUND(AVG(c."Salary")*14) as "Annual_Salary_2_nd_Tech"\
                                 FROM "EMPLOYEE" e JOIN "CONTRACT" c ON e."ID_Employee" = c."ID_Employee" \
                                 WHERE e."Employee_Type" = '+"'Workforce'"+' and CAST(("e"."ID_Employee").id_role as varchar) LIKE ' + "'IDWT2'"+') as tech2,\
                                                \
                                (SELECT ROUND(AVG(c."Salary")*14) as "Annual_Salary_Human_Resources"\
                                 FROM "EMPLOYEE" e JOIN "CONTRACT" c ON e."ID_Employee" = c."ID_Employee" \
                                 WHERE e."Employee_Type" = ' + "'Workforce'"+' and CAST(("e"."ID_Employee").id_role as varchar) LIKE ' + "'IDWHR'"+') as hr,\
                                                \
                                (SELECT ROUND(AVG(c."Salary")*14) as "Annual_Salary_Finance"\
                                 FROM "EMPLOYEE" e JOIN "CONTRACT" c ON e."ID_Employee" = c."ID_Employee" \
                                 WHERE e."Employee_Type" = ' + "'Workforce'"+' and CAST(("e"."ID_Employee").id_role as varchar) LIKE ' + "'IDWFIN'"+') as f,\
                                                \
                                (SELECT ROUND(AVG(c."Salary")*14) as "Annual_Salary_Account_Manager"\
                                 FROM "EMPLOYEE" e JOIN "CONTRACT" c ON e."ID_Employee" = c."ID_Employee" \
                                 WHERE e."Employee_Type" = ' + "'Workforce'"+' and CAST(("e"."ID_Employee").id_role as varchar) LIKE ' + "'IDWAM'"+') as am,\
                                                \
                                (SELECT ROUND(AVG(c."Salary")*14) as "Annual_Salary_Business_Manager"\
                                 FROM "EMPLOYEE" e JOIN "CONTRACT" c ON e."ID_Employee" = c."ID_Employee" \
                                 WHERE e."Employee_Type" = ' + "'Workforce'"+' and CAST(("e"."ID_Employee").id_role as varchar) LIKE ' + "'IDWBM'"+') as bm'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Annual_Salary_CEO', 'Annual_Salary_Leadership', "Annual_Salary_1_st_Tech", "Annual_Salary_2_nd_Tech", "Annual_Salary_Human_Resources", "Annual_Salary_Finance", "Annual_Salary_Account_Manager","Annual_Salary_Business_Manager"]
    print(df)

def Query6_info_Lead():
    print('TASK:  Select the Average Annual Salary of HelpDesk’s Employees have got depending on their Category.')


def Query7_Lead():
    print('RESULT OF THE LEADERSHIP QUERY 7: ')
    Query7_info_Lead()
    cur.execute('SELECT e."ID_Employee", co."ID_Contract", co."Salary"*14 as "Annual_Salary", co."Salary" as "Monthly_Salary", cb."Model_Car", cb."Rent_Price_Car"\
                 FROM "INCLUSION_STOCK_OPTION" iso JOIN "CONTRACT" co ON   iso."ID_Contract" = co."ID_Contract"\
                        JOIN "EMPLOYEE" e ON co."ID_Employee" = e."ID_Employee"\
                        JOIN "INCLUSION_CAR_BENEFIT" icb ON co."ID_Contract" = icb."ID_Contract"\
                        JOIN "CAR_BENEFIT" as cb ON icb."ID_Car_Benefit" = cb."ID_Car_Benefit"\
                 WHERE cb."Horsepower_Car" > 200 and cb."Kilometers_Traveled" < 200000 and co."ID_Benefit_Credit_Card" IS NOT NULL')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'ID_Contract', "Annual_Salary", "Monthly_Salary", "Model_Car", "Rent_Price_Car"]
    print(df)

def Query7_info_Lead():
    print('TASK: Select the ID_Employee, its ID_Contract, its Annual and Monthly Salary, and the model and Rent_Price of its car of an employee that have some Stocks of the Company. Moreover, its car must have more than 200 Horsepower and less than 200000 kilometers traveled. He must also have a Credit Card included in the Contract.')

def Query8_Lead():
    print('RESULT OF THE LEADERSHIP QUERY 8: ')
    Query8_info_Lead()
    cur.execute('SELECT COUNT(fc."ID_Fleet_Company") as "#Car_per_Company", SUM(cb."Rent_Price_Car") as "Sum_Rent_Price", fc."ID_Fleet_Company", fc."Name_Fleet_Company", fc."Address_Fleet_Company"\
                 FROM "FLEET_COMPANY" fc JOIN "CAR_BENEFIT" cb ON fc."ID_Fleet_Company" = cb."ID_Fleet_Company" \
                 GROUP BY fc."ID_Fleet_Company"\
                 HAVING COUNT(fc."ID_Fleet_Company") > 5')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['#Car_per_Company', 'Sum_Rent_Price', "ID_Fleet_Company", "Name_Fleet_Company", "Address_Fleet_Company"]
    print(df)

def Query8_info_Lead():
    print('TASK: Select the Number of Employee’s Cars for every Fleet Company, the sum of the rent price per  Fleet Company, its Id, Name and Address. Return only thosse Fleet Company that have more than 5 cars rented to HelpDesk’s Employees.')



#----------------------------------------------------------------------ACCOUNT_MANAGER------------------------------------------------------------------------------------------------
menu_options_account_manager = {            
                            1: 'Select the average Customer Star got in the Reports in general, by 1_st_Level_Technicians and by 2_nd_Level_Technicians.',
                            2: 'Compose a Ranking of the Technician with the highest average Customer Star got in the Reports, grouped in a Descendent Manner.',
                            3: 'Find the Average Time Intervent for an High-Priority Tickets, Medium-Priority Tickets and Low-Priority Tickets.',
                            4: 'Select the ID, Name, Surname, Level, and Annual Income of the first 5 Account Managers of HelpDesk whose Brand Car is Volkswagen, ordered by annual income. Furthermore find the km travelled with the         Vehicle, the ID of the Fleet company and the Name of the Car.',
                            5: 'Find the total number of Technicians (both of 1st and 2nd level) managed by each Account Manager having more than 7 employee under its control. Order the result in a descendent order.',
                            
                            'Q': 'Exit',
                            'H': 'Help', 
                            'B': 'Back',
                            'L:': 'Go Back to LEADESHIP Working Area (WARNING: Only if you have PERMISSIONS!!!) '
                }

def print_menu_account_manager():
    print('\n \n\nWELCOME TO THE HELPDESK BASIC APPLICATION v_0.1\n')
    print('ACCOUNT MANAGER WORKING AREA:\n')
    for key in menu_options_account_manager.keys():
        print (key, '--', menu_options_account_manager[key] )
        
def Query1_managera():
    print('RESULT OF THE ACCOUNT MANAGER QUERY 1: ')
    Query1_info_managera()
    
    cur.execute('SELECT tot."Average_Customer_Star", st."Average_Customer_Star_1_st_Level_Technician", nd."Average_Customer_Star_2_nd_Level_Technician"\
                FROM(\
                        SELECT AVG(r."Customer_Star") as "Average_Customer_Star_1_st_Level_Technician"\
	 	        FROM "TICKET" ti NATURAL JOIN "REPORT" r\
                        WHERE r."ID_Tech_1" IS NOT NULL AND r."ID_Tech_2" IS NULL AND ti."Closed_Ticket" = True\
		    )  as st, \
		    (\
                        SELECT AVG(r."Customer_Star") as "Average_Customer_Star_2_nd_Level_Technician"\
	 	        FROM "TICKET" ti NATURAL JOIN "REPORT" r\
                        WHERE r."ID_Tech_2" IS NOT NULL AND r."ID_Tech_1" IS NULL AND ti."Closed_Ticket" = True\
		    ) as nd,\
		    (\
                        SELECT AVG("Customer_Star") as "Average_Customer_Star"\
                        FROM "TICKET" NATURAL JOIN "REPORT"\
                        WHERE "Closed_Ticket" = True\
		    )as tot')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Average_Customer_Star', 'Average_Customer_Star_1_st_Level_Technician', "Average_Customer_Star_2_nd_Level_Technician"]
    print(df)

def Query1_info_managera():
    print('TASK: Select the average Customer Star got in the Reports in general, by 1_st_Level_Technicians and by 2_nd_Level_Technicians.\n')
 
def Query2_managera():
    print('RESULT OF THE ACCOUNT MANAGER QUERY 2: ')
    Query2_info_managera()
    
    cur.execute('SELECT *\
                FROM (\
                        SELECT AVG("Customer_Star") as "Customer_Star_Avg", "ID_Tech_2" as "ID_Tech"\
                        FROM "TICKET" NATURAL JOIN "REPORT" \
                        WHERE "Closed_Ticket" = True and  "ID_Tech_2" IS NOT NULL\
                        GROUP BY "ID_Tech_2"\
\
                UNION\
\
                        SELECT AVG("Customer_Star") as "Customer_Star_Avg", "ID_Tech_1" as "ID_Tech"\
                        FROM "TICKET" NATURAL JOIN "REPORT" \
                        WHERE "Closed_Ticket" = True and "ID_Tech_1" IS NOT NULL\
                        GROUP BY "ID_Tech_1"\
                ) as fo\
                ORDER BY "Customer_Star_Avg" DESC')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Customer_Star_Avg', 'ID_Tech']
    print(df)

def Query2_info_managera():
    print('TASK: Compose a Ranking of the Technician with the highest average Customer Star got in the Reports, grouped in a Descendent Manner.\n')   


def Query3_managera():
    print('RESULT OF THE ACCOUNT MANAGER QUERY 3: ')
    Query3_info_managera()
    
    string = 'SELECT * \
              FROM(\
                SELECT ROUND(AVG(report."Time_Intervent")) as "Avg_Time_Intervent_High_Priority"\
                FROM public."TICKET" as ticket\
                INNER JOIN public."REPORT" as report\
                ON report."ID_Ticket" = ticket."ID_Ticket"\
                WHERE ticket."Priority_Ticket" = 1) as high,\
                        \
                (SELECT ROUND(AVG(report."Time_Intervent")) as "Avg_Time_Intervent_Medium_Priority"\
                FROM public."TICKET" as ticket\
                INNER JOIN public."REPORT" as report\
                ON report."ID_Ticket" = ticket."ID_Ticket"\
                WHERE ticket."Priority_Ticket" = 2) as medium,\
                        \
                (SELECT ROUND(AVG(report."Time_Intervent")) as "Avg_Time_Intervent_Low_Priority"\
                FROM public."TICKET" as ticket\
                INNER JOIN public."REPORT" as report\
                ON report."ID_Ticket" = ticket."ID_Ticket"\
                WHERE ticket."Priority_Ticket" = 3) as low'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Avg_Time_Intervent_High_Priority', 'Avg_Time_Intervent_Medium_Priority','Avg_Time_Intervent_Low_Priority']
    print(df)

def Query3_info_managera():
    print('TASK: Find the Average Time Intervent for an High-Priority Tickets, Medium-Priority Tickets and Low-Priority Tickets.\n')

def Query4_managera():
    print('RESULT OF THE ACCOUNT MANAGER QUERY 4: ')
    Query4_info_managera()
    
    string = 'SELECT empl."ID_Employee", empl."Name_Employee", empl."Surname_Employee", empl."Level_Employee", contract."Salary"*14 as "Annual_Income", fleetcom."ID_Fleet_Company", carben."Model_Car", carben."Kilometers_Traveled"\
              FROM public."FLEET_COMPANY" as fleetcom INNER JOIN public."CAR_BENEFIT" as carben ON carben."ID_Fleet_Company" = fleetcom."ID_Fleet_Company"\
                        INNER JOIN public."CONTRACT" as contract ON contract."ID_Car_Benefit" = carben."ID_Car_Benefit"\
                        INNER JOIN public."EMPLOYEE" as empl ON empl."ID_Employee" = contract."ID_Employee"\
                        INNER JOIN public."MANAGER" as manager ON manager."ID_Manager" = empl."ID_Employee"\
              WHERE fleetcom."Name_Fleet_Company" = '+ "'Volkswagen'" +' AND manager."Type_Manager" =' + "'Account Manager'" + '\
              ORDER BY contract."Salary"*14 DESC\
              LIMIT 5'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'Name_Employee', 'Surname_Employee', 'Level_Employee', 'Annual_Income', 'ID_Fleet_Company','Model_Car', 'Kilometers_Traveled']
    print(df)

def Query4_info_managera():
    print('TASK: Select the ID, Name, Surname, Level, and Annual Income of the first 5 Account Managers of HelpDesk whose Brand Car is Volkswagen, ordered by annual income. Furthermore find the km travelled with the Vehicle, the ID of the Fleet company and the Name of the Car.\n')

def Query5_managera():
    print('RESULT OF THE ACCOUNT MANAGER QUERY 5: ')
    Query5_info_managera()
    
    string = 'SELECT tech2_count."ID_Manager", SUM(tech2_count.count_employee + tech1_count.count_employee) as "#Technicians_Controlled" \
              FROM(\
                        SELECT manager."ID_Manager", count(manager."ID_Manager") as count_employee\
                        FROM public."1ST_LEVEL_TECHNICIAN" as tech1\
                        INNER JOIN public."MANAGER" as manager ON tech1."ID_Account_Manager"  = manager."ID_Manager"\
                        GROUP BY manager."ID_Manager") as tech1_count\
                INNER JOIN (\
                        SELECT manager."ID_Manager", count(manager."ID_Manager") as count_employee\
                        FROM public."2ND_LEVEL_TECHNICIAN" as tech2\
                        INNER JOIN public."MANAGER" as manager ON tech2."ID_Account_Manager"  = manager."ID_Manager"\
                        GROUP BY manager."ID_Manager") as tech2_count\
                ON tech2_count."ID_Manager" = tech1_count."ID_Manager"\
            GROUP BY tech2_count."ID_Manager"\
            HAVING SUM(tech2_count.count_employee + tech1_count.count_employee) > 7\
            ORDER BY SUM(tech2_count.count_employee + tech1_count.count_employee) DESC'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Manager', '#Technicians_Controlled']
    print(df)

def Query5_info_managera():
    print('TASK: Find the total number of Technicians (both of 1st and 2nd level) managed by each Account Manager having more than 7 employee under its control. Order the result in a descendent order.\n')
 



#----------------------------------------------------------------------BUSINESS_MANAGER------------------------------------------------------------------------------------------------
menu_options_business_manager = {            
                            1: 'Select the Business Managers ID, Name, Surname, Annual and Monthly Salary that handles a Platinum External Company that has signed a Contract with HelpDesk of an amount greater than 500k.',
                            2: 'Select Business Managers that have either a Gold or Platinum Level, ordered by their current expenses of their Credit Card assigned. Select also some information about the Car they have assigned to.',
                            3: 'Select the Business Manager with the highest amount of bonuses and count how many External Companies are supervised by him.',
                            4: 'Select the ID, Name and Surname of the Business Manager who spent the most with their Credit Card BENEFIT assigned.',
                            5: 'Find the store where the Business Manager may use their foodstamp.',
                            
                            'Q': 'Exit',
                            'H': 'Help',
                            'B': 'Back',
                            'L:': 'Go Back to LEADESHIP Working Area (WARNING: Only if you have PERMISSIONS!!!) ' 
                }

def print_menu_business_manager():
    print('\n \n\nWELCOME TO THE HELPDESK BASIC APPLICATION v_0.1\n')
    print('BUSINESS MANAGER WORKING AREA:\n')
    for key in menu_options_business_manager.keys():
        print (key, '--', menu_options_business_manager[key] )

def Query1_managerb():
    print('RESULT OF THE BUSINESS MANAGER QUERY 1: ')
    Query1_info_managerb()
    
    string = 'SELECT DISTINCT empl."ID_Employee", empl."Name_Employee", empl."Surname_Employee", contract."Salary", (contract."Salary" * 14) as "Annual_Income", extcomp."External_Company_Name", extcontract."Amount_Contract"\
                 FROM "EXTERNAL_COMPANY" as extcomp INNER JOIN "EXTERNAL_CONTRACT" as extcontract ON extcontract."ID_External_Company" = extcomp."ID_External_Company"\
		        INNER JOIN "EMPLOYEE" as empl ON empl."ID_Employee" = extcomp."ID_Business_Manager"\
		        INNER JOIN "CONTRACT" as contract ON contract."ID_Employee" = empl."ID_Employee"\
                 WHERE extcomp."External_Company_Level" = ' + "'Platinum'" + 'AND extcontract."Amount_Contract" > 500000'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'Name_Employee', "Surname_Employee", 'Salary', 'Annual_Income', 'External_Company_Name', 'Amount_Contract']
    print(df)

def Query1_info_managerb():
    print('TASK: Select the Business Managers ID, Name, Surname, Annual and Monthly Salary that handles a Platinum External Company that has signed a Contract with HelpDesk of an amount greater than 500k.\n')

def Query2_managerb():
    print('RESULT OF THE BUSINESS MANAGER QUERY 2: ')
    Query2_info_managerb()
    
    string = 'SELECT empl."ID_Employee", empl."Name_Employee", empl."Surname_Employee", cc."Current_Expense" as "Current_Expense_Credit_Card",fleetcom."Name_Fleet_Company", carben."Model_Car", carben."Kilometers_Traveled", empl."Level_Employee", carben."Rent_Expiry_Date"\
                FROM public."FLEET_COMPANY" as fleetcom INNER JOIN public."CAR_BENEFIT" as carben ON carben."ID_Fleet_Company" = fleetcom."ID_Fleet_Company"\
                        INNER JOIN public."CONTRACT" as contract ON contract."ID_Car_Benefit" = carben."ID_Car_Benefit"\
                        INNER JOIN public."EMPLOYEE" as empl ON empl."ID_Employee" = contract."ID_Employee"\
                        INNER JOIN public."MANAGER" as manager ON manager."ID_Manager" = empl."ID_Employee"\
                        INNER JOIN "CREDIT_CARD" as cc ON cc."ID_Benefit_Credit_Card" = contract."ID_Benefit_Credit_Card"\
                WHERE carben."Rent_Expiry_Date" >= now() AND CAST(("empl"."ID_Employee").id_role as varchar) LIKE '+ "'IDWBM'" + ' AND (empl."Level_Employee" = ' + "'Platinum'" +'or empl."Level_Employee" ='+" 'Gold')" + '\
                ORDER BY cc."Current_Expense" DESC'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'Name_Employee', "Surname_Employee", 'Current_Expense_Credit_Card', 'Name_Fleet_Company', 'Model_Car', 'Kilometers_Traveled', 'Level_Employee', 'Rent_Expiry_Date']
    print(df)

def Query2_info_managerb():
    print('TASK: Select Business Managers that have either a Gold or Platinum Level, ordered by their current expenses of their Credit Card assigned. Select also some information about the Car they have assigned to.\n')
 
def Query3_managerb():
    print('RESULT OF THE BUSINESS MANAGER QUERY 3: ')
    Query3_info_managerb()
    
    string = 'SELECT *\
              FROM (\
                        SELECT MAX(contract."Bonus") as max_bonus, extcom."ID_Business_Manager", COUNT(extcom."ID_External_Company") as count_company\
                        FROM "EXTERNAL_COMPANY" as extcom INNER JOIN "CONTRACT" as contract ON extcom."ID_Business_Manager" = contract."ID_Employee"\
                        WHERE contract."Bonus"  IS NOT NULL \
                        GROUP BY extcom."ID_Business_Manager"\
                        ORDER BY max_bonus DESC) as temp1\
              WHERE temp1."max_bonus" = ( \
                        SELECT temp2."max_bonus" \
                        FROM (\
                                        SELECT MAX(contract."Bonus") as max_bonus, extcom."ID_Business_Manager"\
                                        FROM "EXTERNAL_COMPANY" as extcom LEFT JOIN "CONTRACT" as contract ON extcom."ID_Business_Manager" = contract."ID_Employee"\
                        WHERE contract."Bonus"  IS NOT NULL \
                        GROUP BY extcom."ID_Business_Manager"\
                        ORDER BY max_bonus DESC  LIMIT 1 ) as temp2\
                )'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['max_bonus', 'ID_Business_Manager', "count_company"]
    print(df)

def Query3_info_managerb():
    print('TASK: Select the Business Manager  with the highest amount of bonuses and count how many External Companies are supervised by him.\n')
    
def Query4_managerb():
    print('RESULT OF THE BUSINESS MANAGER QUERY 4: ')
    Query4_info_managerb()
    
    string = 'SELECT *\
              FROM (\
                        SELECT cc."Current_Expense", contract."ID_Employee", empl."Name_Employee", empl."Surname_Employee"\
                        FROM public."EMPLOYEE" as empl INNER JOIN public."CONTRACT" as contract ON contract."ID_Employee" = empl."ID_Employee"\
                        INNER JOIN public."CREDIT_CARD" as cc ON cc."ID_Benefit_Credit_Card" = contract."ID_Benefit_Credit_Card"\
                        WHERE CAST((contract."ID_Employee").id_role as varchar) LIKE '+ "'IDWBM'" + '\
                        ORDER BY cc."Current_Expense" DESC) as temp1\
              WHERE temp1."Current_Expense" = ( \
                        SELECT temp2."Current_Expense" \
                        FROM (\
                                SELECT cc."Current_Expense", contract."ID_Employee" \
                                FROM public."EMPLOYEE" as empl INNER JOIN public."CONTRACT" as contract ON contract."ID_Employee" = empl."ID_Employee"\
                                        INNER JOIN public."CREDIT_CARD" as cc ON cc."ID_Benefit_Credit_Card" = contract."ID_Benefit_Credit_Card"\
                                WHERE CAST((contract."ID_Employee").id_role as varchar) LIKE ' + "'IDWBM'" + '\
                                ORDER BY cc."Current_Expense" DESC  LIMIT 1 ) as temp2\
                )'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Current_Expense', 'ID_Employee', 'Name_Employee', 'Surname_Employee']
    print(df)

def Query4_info_managerb():
    print('TASK: Select the ID, Name and Surname of the Business Manager who spent the most with their Credit Card BENEFIT assigned.\n')
 
def Query5_managerb():
    print('RESULT OF THE BUSINESS MANAGER QUERY 5: ')
    Query5_info_managerb()
    
    string = 'SELECT contract."ID_Employee", inclfood."ID_Benefit_Food_Stamp", affiliation."ID_Store", store."Name_Store"\
              FROM public."CONTRACT" as contract INNER JOIN public."INCLUSION_FOOD_STAMP" as inclfood ON inclfood."ID_Contract" = contract."ID_Contract"\
                        INNER JOIN public."AFFILIATION" as affiliation ON affiliation."ID_Benefit_Food_Stamp" = inclfood."ID_Benefit_Food_Stamp"\
                        INNER JOIN public."STORE" as store ON store."ID_Store" = affiliation."ID_Store"\
              WHERE CAST((contract."ID_Employee").id_role as varchar) LIKE'+" 'IDWBM'" 
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'ID_Benefit_Food_Stamp', 'ID_Store', 'Name_Store']
    print(df)

def Query5_info_managerb():
    print('TASK: Find the store where the Business Manager may use their foodstamp.\n')
 

#----------------------------------------------------------------------FINANCE------------------------------------------------------------------------------------------------
menu_options_finance= {            
                            1: 'Select the Total Amount that a particular External Company, cumulating the External Company Contract, selecting only those External Company that bring a Cumulative Income greater than 500k.',
                            2: 'Select the ID of the Finance Employee who defined the details of the oldest Contract signed by an External Contract.',
                            3: 'Select the number of Tickets(that need to be more than two) opened by Customers related to a product that belongs to the Biggest External Company Client(Platinum Level).',
                            4: 'For each Finance employee find out how many money HelpDesk has to spend for his/her technological benefits, both singularly both as a whole, and express the model of these benefit and their technology       company.',
                            5: 'Select the Financer ID, Name, Surname, Annual and Monthly Salary that have closed a deal with a Platinum External Company that has signed a Contract with HelpDesk of an amount greater than 500k.',
                            
                            'Q': 'Exit',
                            'H': 'Help' ,
                            'B': 'Back', 
                            'L:': 'Go Back to LEADESHIP Working Area (WARNING: Only if you have PERMISSIONS!!!) '
                }

def print_menu_finance():
    print('\n \n\nWELCOME TO THE HELPDESK BASIC APPLICATION v_0.1\n')
    print('FINANCE WORKING AREA:\n')
    for key in menu_options_finance.keys():
        print (key, '--', menu_options_finance[key] )
        
def Query1_Finance():
    print('RESULT OF THE FINANCE QUERY 1: ')
    Query1_info_Finance()
    
    cur.execute('SELECT SUM(con."Amount_Contract") as "Cumulative_Income", exco."ID_External_Company", exco."External_Company_Name"\
                 FROM "EXTERNAL_COMPANY" exco JOIN "EXTERNAL_CONTRACT" con ON exco."ID_External_Company" = con."ID_External_Company"\
                 GROUP BY exco."ID_External_Company" \
                 HAVING SUM(con."Amount_Contract")> 500000 \
                 ORDER BY SUM(con."Amount_Contract") DESC')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Cumulative_Income', 'ID_External_Company', 'External_Company_Name']
    print(df)

def Query1_info_Finance():
    print('TASK: Select the Total Amount that a particular External Company, cumulating the External Company Contract, selecting only those External Company that bring a Cumulative Income greater than 500k.\n')   

def Query2_Finance():
    print('RESULT OF THE FINANCE QUERY 2: ')
    Query2_info_Finance()
    
    cur.execute('SELECT "ID_Finance_Employee"\
                 FROM "EXTERNAL_CONTRACT" \
                 WHERE "ID_External_Contract" = (\
                        SELECT ec."ID_External_Contract"\
                        FROM "EXTERNAL_CONTRACT" as ec\
                        WHERE ec."Date_Time_Signature_External_Contract" = (\
                                SELECT MIN( "Date_Time_Signature_External_Contract" )\
                                FROM "EXTERNAL_CONTRACT"\
		)\
	)')
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Finance_Employee']
    print(df)

def Query2_info_Finance():
    print('TASK: Select the ID of the Finance Employee who defined the details of the oldest Contract signed by an External Contract. \n')   

def Query3_Finance():
    print('RESULT OF THE FINANCE QUERY 3: ')
    Query3_info_Finance()
    
    string = 'SELECT COUNT(ticket."ID_Ticket") as Count_Ticket, extcom."ID_External_Company", extcom."External_Company_Name", extcom."External_Company_Level"\
                 FROM public."TICKET" as ticket INNER JOIN "PRODUCT" as product ON product."ID_Product" = ticket."ID_Product"\
                        INNER JOIN "EXTERNAL_COMPANY" as extcom ON extcom."ID_External_Company" = product."ID_External_Company"\
                 WHERE extcom."External_Company_Level" = ' + "'Platinum'" + '\
                 GROUP BY extcom."ID_External_Company"\
                 HAVING COUNT(ticket."ID_Ticket") > 2'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Count_Ticket', 'ID_External_Company', 'External_Company_Name', 'External_Company_Level']
    print(df)

def Query3_info_Finance():
    print('TASK: Select the number of Tickets(that need to be more than two) opened by Customers related to a product that belongs to the Biggest External Company Client(Platinum Level).\n')   

def Query4_Finance():
    print('RESULT OF THE FINANCE QUERY 4: ')
    Query4_info_Finance()
    
    string = 'SELECT contract."ID_Employee", phoneben."Model_Phone_Benefit", phoneben."Price_Phone", phoneben."Brand_Phone", pcben."Model_PC_Benefit",pcben."Price_PC", pcben."Brand_PC",(phoneben."Price_Phone" + pcben."Price_PC") as "Total_Expenses"\
              FROM public."CONTRACT" as contract INNER JOIN public."PHONE_BENEFIT" as phoneben ON phoneben."ID_Benefit_Phone_Benefit" = contract."ID_Phone_Benefit"\
	                INNER JOIN public."PC_BENEFIT" as pcben ON pcben."ID_Benefit_PC_Benefit" = contract."ID_PC_Benefit"\
              WHERE CAST(("contract"."ID_Employee").id_role as varchar) LIKE ' + "'IDWFIN';"
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'Model_Phone_Benefit', 'Price_Phone', 'Brand_Phone', 'Model_PC_Benefit', 'Price_PC', 'Brand_PC', 'Total_Expenses']
    print(df)

def Query4_info_Finance():
    print('TASK: For each Finance employee find out how many money HelpDesk has to spend for his/her technological benefits, both singularly both as a whole, and express the model of these benefit and their technology company.\n')   


def Query5_Finance():
    print('RESULT OF THE FINANCE QUERY 5: ')
    Query5_info_Finance()
    
    string = 'SELECT e."ID_Employee", e."Name_Employee", e."Surname_Employee", contract."Salary", (contract."Salary"* 14) as "Annual_Income", eco."External_Company_Name", ec."Amount_Contract" \
              FROM "EXTERNAL_CONTRACT" as ec JOIN "EMPLOYEE" as e ON ec."ID_Finance_Employee" = e."ID_Employee"\
                        JOIN "EXTERNAL_COMPANY" as eco ON ec."ID_External_Company" = eco."ID_External_Company"\
                        JOIN "CONTRACT" contract ON e."ID_Employee" = contract."ID_Employee"\
              WHERE eco."External_Company_Level" = ' + "'Platinum'" + 'and ec."Amount_Contract" > 500000'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'Name_Employee', 'Surname_Employee', 'Salary', 'Annual_Income', 'External_Company_Name', 'Amount_Contract']
    print(df)

def Query5_info_Finance():
    print('TASK: Select the Financer ID, Name, Surname, Annual and Monthly Salary that have closed a deal with a Platinum External Company that has signed a Contract with HelpDesk of an amount greater than 500k.\n')   

#----------------------------------------------------------------------1_ST_LEVEL_TECHNICIAN------------------------------------------------------------------------------------------------
menu_options_1_st_tech = {            
                            1: 'Find the ID, the name, the bonus value, the average Customer star and the remaining holidays of the 1st level Technicians who ever managed a Ticket ordered in a Crescent manner basing on their Customer      Star',
                            2: 'Select the ID of the Account Managers, of that 1st level Technicians who have closed a ticket. Count also the number of Tickets that have been closed under him/her responsibility.', 
                            3: 'Insert in the Report all the ID Customer and personal data of 1st Level   Technicians that have closed a ticket without delegating to a 2nd Level Technicians.',
                            4: 'Select all the Course Companies that have released a certification to a 1st Level Technicians in the last year, and the number of certification released to them. ',
                            5: 'Find the Customer Star, the Customer Feedback, the Level and the Salary about the 1st Level Technicians that earn more than 1200 euros at month and that are not Metal Level, who managed a Report without     delegating.',
                            
                            'Q': 'Exit',
                            'H': 'Help',
                            'B': 'Back', 
                            'L:': 'Go Back to LEADESHIP Working Area (WARNING: Only if you have PERMISSIONS!!!) ' 
                }

def print_menu_tech1():
    print('\n \n\nWELCOME TO THE HELPDESK BASIC APPLICATION v_0.1\n')
    print('1 ST LEVEL TECHNICIAN WORKING AREA:\n')
    for key in menu_options_1_st_tech.keys():
        print (key, '--', menu_options_1_st_tech[key] )
        
def Query1_tech1():
    print('RESULT OF THE 1 ST LEVEL TECHNICIAN QUERY 1: ')
    Query1_info_tech1()
    
    string = 'SELECT empl."ID_Employee", empl."Name_Employee", contract."Bonus", AVG(report."Customer_Star") as average_customer_star, contract."Holidays_Left", report."ID_Ticket"\
                 FROM "EMPLOYEE" as empl INNER JOIN "CONTRACT" as contract ON contract."ID_Employee" = empl."ID_Employee" \
	                INNER JOIN public."REPORT" as report ON report."ID_Tech_1" = empl."ID_Employee" OR report."ID_Tech_2" = empl."ID_Employee"\
                 WHERE CAST(("empl"."ID_Employee").id_role as varchar) LIKE '+"'IDWT1'"+' \
                 GROUP BY empl."ID_Employee", empl."Name_Employee", contract."Bonus", report."Customer_Star", contract."Holidays_Left", report."ID_Ticket"\
                 ORDER BY average_customer_star asc'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'Name_Employee', 'Bonus', 'average_customer_star', 'Holidays_Left', 'ID_Ticket']
    print(df)

def Query1_info_tech1():
    print('TASK: Find the ID, the name, the bonus value, the average Customer star and the remaining holidays of the 1st level Technicians who ever managed a Ticket ordered in a Crescent manner basing on their Customer Star\n')   

def Query2_tech1():
    print('RESULT OF THE 1 ST LEVEL TECHNICIAN QUERY 2:  ')
    Query2_info_tech1()
    
    string = 'SELECT tech1."ID_Account_Manager", empl."Name_Employee", ticket."ID_Ticket", tech1."ID_Tech_1", COUNT(tech1."ID_Tech_1") as "#Closed_Ticket"\
              FROM public."TICKET" as ticket INNER JOIN public."REPORT" as report ON ticket."ID_Ticket" = report."ID_Ticket" \
                INNER JOIN public."1ST_LEVEL_TECHNICIAN" as tech1 ON tech1."ID_Tech_1" = report."ID_Tech_1"\
                INNER JOIN  public."EMPLOYEE" as empl ON tech1."ID_Account_Manager" =  empl."ID_Employee"\
              WHERE ticket."Closed_Ticket" = true\
              GROUP BY tech1."ID_Account_Manager", empl."Name_Employee", ticket."Closed_Ticket", ticket."ID_Ticket", tech1."ID_Tech_1", tech1."ID_Tech_1"'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Account_Manager', 'Name_Employee', 'ID_Ticket','ID_Tech_1', '#Closed_Ticket']
    print(df)
    
def Query2_info_tech1():
    print('TASK: Select the ID of the Account Managers, of that 1st level Technicians who have closed a ticket. Count also the number of Tickets that have been closed under him/her responsibility.\n')

def Query3_tech1():
    print('RESULT OF THE 1 ST LEVEL TECHNICIAN QUERY 3:  ')
    Query3_info_tech1()
    
    string = 'SELECT report."ID_Customer", empl."Name_Employee", empl."Surname_Employee", report."ID_Tech_1", phone."Number_Employee", address."Address_Empl",email."Email_Address_Employee", ticket."Closed_Ticket"\
              FROM public."REPORT" as report INNER JOIN public."EMPLOYEE" as empl ON empl."ID_Employee" = report."ID_Tech_1"\
                INNER JOIN public."PHONE_EMPLOYEE" as phone ON phone."ID_Employee" = empl."ID_Employee"\
                INNER JOIN public."ADDRESS_EMPLOYEE" as address ON address."ID_Employee" = empl."ID_Employee"\
                INNER JOIN public."EMAIL_EMPLOYEE" as email ON email."ID_Employee" = empl."ID_Employee"\
                INNER JOIN public."TICKET" as ticket ON ticket."ID_Ticket" = report."ID_Ticket"\
              WHERE ticket."Closed_Ticket" = true'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Customer', 'Name_Employee', 'Surname_Employee', 'ID_Tech_1', 'Number_Employee', 'Address_Empl', 'Email_Address_Employee', 'Closed_Ticket']
    print(df)


def Query3_info_tech1():
    print('TASK: Insert in the Report all the ID Customer and personal data of 1st Level   Technicians that have closed a ticket without delegating to a 2nd Level Technicians..\n')

def Query4_tech1():
    print('RESULT OF THE 1 ST LEVEL TECHNICIAN QUERY 4:  ')
    Query4_info_tech1()
    
    string = 'SELECT DISTINCT cert."ID_Course_Company", coursecom."Name_Course_Company", COUNT(cert."ID_Certification") as "#Certification_Released"\
              FROM public."ACHIEVEMENT_CERTIFICATION" as  achcert INNER JOIN public."EMPLOYEE" as empl ON empl."ID_Employee" = achcert."ID_Employee"\
                INNER JOIN public."CERTIFICATION" as cert ON cert."ID_Certification" = achcert."ID_Certification"\
                INNER JOIN public."COURSE_COMPANY" as coursecom ON coursecom."ID_Course_Company" = cert."ID_Course_Company"\
              WHERE CAST((empl."ID_Employee").id_role as varchar) LIKE '+ "'IDWT1'" + 'and "Date_Time_Certification" > current_date - interval '+ "'1 year'" +'\
              GROUP BY cert."ID_Course_Company", coursecom."Name_Course_Company", cert."ID_Certification"'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Course_Company', 'Name_Course_Company', '#Certification_Released']
    print(df)

def Query4_info_tech1():
    print('TASK: Select all the Course Companies that have released a certification to a 1st Level Technicians in the last year, and the number of certification released to them. .\n')
    
def Query5_tech1():
    print('RESULT OF THE 1 ST LEVEL TECHNICIAN QUERY 5:  ')
    Query5_info_tech1()
    
    string = 'SELECT report."Customer_Star", report."Customer_Feedback", empl."Name_Employee", empl."Surname_Employee",  report."ID_Tech_1",contract."Salary"\
              FROM "REPORT" as report INNER JOIN public."EMPLOYEE" as empl ON empl."ID_Employee" = report."ID_Tech_1"\
	        INNER JOIN public."CONTRACT" as contract ON contract."ID_Employee" = empl."ID_Employee"\
              WHERE contract."Salary" > 1200 and "Level_Employee" !='+ "'Metal'"
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Customer_Star', 'Customer_Feedback', 'Name_Employee', 'Surname_Employee', 'ID_Tech_1','Salary']
    print(df)

def Query5_info_tech1():
    print('TASK: Find the Customer Star, the Customer Feedback, the Level and the Salary about the 1st Level Technicians that earn more than 1200 euros at month and that are not Metal Level, who managed a Report without delegating.\n')

#----------------------------------------------------------------------2_ND_LEVEL_TECHNICIAN------------------------------------------------------------------------------------------------
menu_options_2_nd_tech = {            
                            1: 'Find the personal data of all the 2nd Level Technicians who compiled a Report.',
                            2: 'Find the ID, the name, the bonus value, the average Customer star and the remaining holidays of the 2nd level Technicians who ever managed a Ticket ordered in a Crescent manner basing on their Customer      Star.',
                            3: 'Find the Model of vehicles used by the Technicians to solve the problems on site, and for each Technician assigned to a Van which have traveled for at least 30000 km, find the amount of Current Expense,     made with the Credit Card, average of his/her Customer Star, the bonus received and his/her salary.',
                            4: 'Find all the PPE used by the 2nd Level Technicians who used a vehicle of the Fleet Company Citroën',
                            5: 'For each 2nd Level technician find out how many money HelpDesk has spent for his/her technological benefits, and express the model of these benefit and their technology company.',
                            
                            'Q': 'Exit',
                            'H': 'Help',
                            'B': 'Back',
                            'L:': 'Go Back to LEADESHIP Working Area (WARNING: Only if you have PERMISSIONS!!!) ' 
                }

def print_menu_tech2():
    print('\n \n\nWELCOME TO THE HELPDESK BASIC APPLICATION v_0.1\n')
    print('2 ND LEVEL TECHNICIAN WORKING AREA:\n')
    for key in menu_options_2_nd_tech.keys():
        print (key, '--', menu_options_2_nd_tech[key] )
        
def Query1_tech2():
    print('RESULT OF THE 2 ND LEVEL TECHNICIAN QUERY 1:  ')
    Query1_info_tech2()
    
    string = 'SELECT phone."Number_Employee", address."Address_Empl",report."ID_Tech_2", empl."Name_Employee", empl."Surname_Employee", empl."Number_Bank_Account"\
              FROM public."REPORT" as report INNER JOIN public."EMPLOYEE" as empl	ON empl."ID_Employee" = report."ID_Tech_2" \
                INNER JOIN public."PHONE_EMPLOYEE" as phone ON phone."ID_Employee" = empl."ID_Employee"\
                INNER JOIN public."ADDRESS_EMPLOYEE" as address ON address."ID_Employee" = empl."ID_Employee"'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Number_Employee', 'Address_Empl', 'ID_Tech_2', 'Name_Employee', 'Surname_Employee', 'Number_Bank_Account']
    print(df)

def Query1_info_tech2():
    print('TASK: Find the personal data of all the 2nd Level Technicians who compiled a Report.\n')

def Query2_tech2():
    print('RESULT OF THE 2 ND LEVEL TECHNICIAN QUERY 2:  ')
    Query2_info_tech2()
    
    string = 'SELECT empl."ID_Employee", empl."Name_Employee", contract."Bonus", AVG(report."Customer_Star") as "Average_Customer_Star", contract."Holidays_Left", report."ID_Ticket"\
              FROM public."EMPLOYEE" as empl INNER JOIN public."CONTRACT" as contract ON contract."ID_Employee" = empl."ID_Employee"\
	        INNER JOIN public."REPORT" as report ON report."ID_Tech_1" = empl."ID_Employee" OR report."ID_Tech_2" = empl."ID_Employee"\
              WHERE CAST(("empl"."ID_Employee").id_role as varchar) LIKE'+ "'IDWT1'"+'OR CAST(("empl"."ID_Employee").id_role as varchar) LIKE '+"'IDWT2'" + '\
              GROUP BY empl."ID_Employee", empl."Name_Employee", contract."Bonus", report."Customer_Star", contract."Holidays_Left", report."ID_Ticket"\
              ORDER BY "Average_Customer_Star" ASC'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'Name_Employee', 'Bonus','Average_Customer_Star', 'Holidays_Left', 'ID_Ticket']
    print(df)

def Query2_info_tech2():
    print('TASK: Find the ID, the name, the bonus value, the average Customer star and the remaining holidays of the 2nd level Technicians who ever managed a Ticket ordered in a Crescent manner basing on their Customer Star.\n')

def Query3_tech2():
    print('RESULT OF THE 2 ND LEVEL TECHNICIAN QUERY 3:  ')
    Query3_info_tech2()
    
    string = 'SELECT fleetcom."ID_Fleet_Company", vehicle."Plate_Number", vehicle."Model_Vehicle", cc."Current_Expense", vehicle."Kilometers_Travelled" as "Kilometers_Traveled", contract."Bonus", contract."Salary", tech2."ID_Tech_2"\
              FROM "FLEET_COMPANY" AS fleetcom INNER JOIN public."VEHICLE" as vehicle ON vehicle."ID_Fleet_Company" = fleetcom."ID_Fleet_Company"\
                INNER JOIN public."DRIVE_VEHICLE" as drivevehicle ON drivevehicle."ID_Vehicle" = vehicle."Plate_Number"\
                INNER JOIN public."2ND_LEVEL_TECHNICIAN" as tech2 ON tech2."ID_Tech_2" = drivevehicle."ID_Tech_2"\
                INNER JOIN "EMPLOYEE" as empl ON empl."ID_Employee" = tech2."ID_Tech_2"\
                INNER JOIN "CONTRACT" as contract ON contract."ID_Employee" = empl."ID_Employee"\
                INNER JOIN "CREDIT_CARD" as cc ON cc."ID_Benefit_Credit_Card" = contract."ID_Benefit_Credit_Card"\
             WHERE vehicle."Vehicle_Type" = '+"'Van'"+'and vehicle."Kilometers_Travelled" > 30000'

    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Fleet_Company', 'Plate_Number', 'Model_Vehicle', 'Current_Expense', 'Kilometers_Traveled', 'Bonus', 'Salary', 'ID_Tech_2']
    print(df)

def Query3_info_tech2():
    print('TASK: Find the Model of vehicles used by the Technicians to solve the problems on site, and for each Technician assigned to a Van which have traveled for at least 30000 km,  find the amount of Current Expense, made with the Credit Card, average of his/her Customer Star, the bonus received and his/her salary.\n')

def Query4_tech2():
    print('RESULT OF THE 2 ND LEVEL TECHNICIAN QUERY 4:  ')
    Query4_info_tech2()
    
    string = 'SELECT ppe."Type_PPE", drveh."ID_Vehicle", ppeass."ID_PPE", vehicle."Model_Vehicle", vehicle."ID_Fleet_Company", vehicle."Brand_Vehicle"\
              FROM  public."PPE" as ppe INNER JOIN public."PPE_ASSIGNED" as ppeass ON ppeass."ID_PPE" = ppe."ID_PPE"\
                INNER JOIN public."DRIVE_VEHICLE" as drveh ON drveh."ID_Tech_2" = ppeass."ID_Tech_2"\
                INNER JOIN public."VEHICLE" as vehicle ON vehicle."Plate_Number" = drveh."ID_Vehicle"\
              WHERE vehicle."Brand_Vehicle" = '+"'Citroën'"
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Type_PPE', 'ID_Vehicle', 'ID_PPE', 'Model_Vehicle', 'ID_Fleet_Company', 'Brand_Vehicle']
    print(df)

def Query4_info_tech2():
    print('TASK: Find all the PPE used by the 2nd Level Technicians who used a vehicle of the Fleet Company Citroën.\n')

def Query5_tech2():
    print('RESULT OF THE 2 ND LEVEL TECHNICIAN QUERY 5:  ')
    Query5_info_tech2()
    
    string = 'SELECT contract."ID_Employee", ipadben."Model_Ipad_Benefit", ipadben."Price_IPAD", ipadben."Brand_IPAD"\
              FROM public."CONTRACT" as contract INNER JOIN public."IPAD_BENEFIT" as ipadben ON ipadben."ID_Benefit_IPAD_Benefit" = contract."ID_IPAD_Benefit"\
              WHERE CAST((contract."ID_Employee").id_role as varchar) LIKE ' + "'IDWT2'"
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Employee', 'Model_Ipad_Benefit', 'Price_IPAD', 'Brand_IPAD']
    print(df)

def Query5_info_tech2():
    print('TASK: For each 2nd Level technician find out how many money HelpDesk has spent for his/her technological benefits, and express the model of these benefit and their technology company.\n')
#----------------------------------------------------------------------HUMAN_RESOURCES------------------------------------------------------------------------------------------------
menu_options_hr = {            
                            1: 'Select the name, the email and the phone number of the HR who watched the Tickets and if the Ticket has been closed, check in how much time the issue has been solved basing on the report information.',
                            2: 'Find the amount of the Contract handled by the HR employee that have received the highest number of Bonus.',
                            3: 'Select in a descendent order the first 15 name of the employees and the ID of the HR employee who hired them, who still have more than 13 days of holidays left depending on the number of days of             holidays left.',
                            4: 'Find all the email, name and surname HR who have a phone benefit of the brand "Samsung" and their annual salary is beyond the 25 k treshold. Order the result by descendent Annual Salary.',
                            5: 'Find the ranking of the HR basing on how many employee they have hired specifying their name and surname, ordering in descending order w.r.t. the number of employee hired.',
                            
                            'Q': 'Exit',
                            'H': 'Help',
                            'B': 'Back',
                            'L:': 'Go Back to LEADESHIP Working Area (WARNING: Only if you have PERMISSIONS!!!) ' 
                }

def print_menu_hr():
    print('\n \n\nWELCOME TO THE HELPDESK BASIC APPLICATION v_0.1\n')
    print('HUMAN RESOURCES WORKING AREA:\n')
    for key in menu_options_hr.keys():
        print (key, '--', menu_options_hr[key] )

def Query1_hr():
    print('RESULT OF THE HUMAN RESOURCES QUERY 1:  ')
    Query1_info_hr()
    
    string = 'SELECT empl."Name_Employee", emailempl."Email_Address_Employee", empl."ID_Employee", phoneempl."Number_Employee", viewticket."ID_Ticket", ticket."Priority_Ticket", ticket."Closed_Ticket", \
              CASE WHEN ticket."Closed_Ticket" THEN report."Time_Intervent" ELSE NULL END as closed\
              FROM "EMPLOYEE" as empl INNER JOIN public."PHONE_EMPLOYEE" as phoneempl ON phoneempl."ID_Employee" = empl."ID_Employee"\
                        INNER JOIN public."EMAIL_EMPLOYEE" as emailempl ON emailempl."ID_Employee" = empl."ID_Employee"\
                        INNER JOIN public."VIEWING_TICKET" as viewticket ON viewticket."ID_Employee" = empl."ID_Employee"\
                        INNER JOIN public."TICKET" as ticket ON viewticket."ID_Ticket" = ticket."ID_Ticket"\
                        INNER JOIN public."REPORT" as report ON report."ID_Ticket" = ticket."ID_Ticket"\
              WHERE  CAST(("empl"."ID_Employee").id_role as varchar) LIKE '+"'IDWHR'"
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Name_Employee', 'Email_Address_Employee', 'ID_Employee', 'Number_Employee', 'ID_Ticket', 'Priority_Ticket', 'Closed_Ticket', 'Time_Intervent']
    print(df)

def Query1_info_hr():
    print('TASK: Select the name, the email and the phone number of the HR who watched the Tickets and if the Ticket has been closed, check in how much time the issue has been solved basing on the report information..\n')

def Query2_hr():
    print('RESULT OF THE HUMAN RESOURCES QUERY 2:  ')
    Query2_info_hr()
    
    string = 'SELECT *\
              FROM (\
                        SELECT MAX(contract."Bonus") as max_bonus, empl."ID_Human_Resources", COUNT(empl."ID_Employee") as count_contract\
                        FROM public."EMPLOYEE" as empl INNER JOIN "CONTRACT" as contract ON empl."ID_Human_Resources" = contract."ID_Employee"\
                        WHERE contract."Bonus"  IS NOT NULL \
                        GROUP BY empl."ID_Human_Resources"\
                        ORDER BY max_bonus DESC) as temp1\
             WHERE temp1."max_bonus" = ( \
                        SELECT temp2."max_bonus" FROM (\
                                        SELECT MAX(contract."Bonus") as max_bonus, empl."ID_Human_Resources"\
                                        FROM public."EMPLOYEE" as empl INNER JOIN "CONTRACT" as contract ON empl."ID_Human_Resources" = contract."ID_Employee"\
                                        WHERE contract."Bonus"  IS NOT NULL \
                                        GROUP BY empl."ID_Human_Resources"\
                                        ORDER BY max_bonus DESC  LIMIT 1 ) as temp2\
                )'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Max_Bonus', 'ID_Human_Resources', "Count_Contract"]
    print(df)

def Query2_info_hr():
    print('TASK: Find the amount of the Contract handled by the HR employee that have received the highest number of Bonus.\n')

def Query3_hr():
    print('RESULT OF THE HUMAN RESOURCES QUERY 3:  ')
    Query3_info_hr()
    
    string = 'SELECT contract."Holidays_Left", empl."ID_Employee", empl."Name_Employee", empl."Surname_Employee", contract."Salary"*14 as "Annual_Salary", empl."ID_Human_Resources" \
              FROM public."EMPLOYEE" as empl INNER JOIN public."CONTRACT" as contract ON contract."ID_Employee" = empl."ID_Employee"\
              WHERE contract."Holidays_Left" > 13 AND empl."ID_Human_Resources" IS NOT NULL\
              ORDER BY contract."Holidays_Left" DESC\
              LIMIT 15'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Holidays_Left', 'ID_Employee', 'Name_Employee', 'Surname_Employee', 'Annual_Salary', 'ID_Human_Resources']
    print(df)

def Query3_info_hr():
    print('TASK: Select in a descendent order the first 15 name of the employees and the ID of the HR employee who hired them, who still have more than 13 days of holidays left depending on the number of days of holidays left.\n')

def Query4_hr():
    print('RESULT OF THE HUMAN RESOURCES QUERY 4:  ')
    Query4_info_hr()
    
    string = 'SELECT phone."Model_Phone_Benefit", contract."ID_Phone_Benefit", email."Email_Address_Employee",  empl."ID_Employee", empl."Name_Employee", (contract."Salary")*14 as "Annual_Income"\
              FROM public."PHONE_BENEFIT" as phone INNER JOIN public."CONTRACT" as contract ON contract."ID_Phone_Benefit" = phone."ID_Benefit_Phone_Benefit"\
                        INNER JOIN public."EMPLOYEE" as empl ON empl."ID_Employee" = contract."ID_Employee"\
                        INNER JOIN public."EMAIL_EMPLOYEE" as email ON email."ID_Employee" = empl."ID_Employee"\
              WHERE phone."Brand_Phone" = ' +"'Samsung'"+ ' and (contract."Salary")*14 > 25000\
              ORDER BY (contract."Salary")*14 DESC'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['Model_Phone_Benefit', 'ID_Phone_Benefit', 'Email_Address_Employee', 'ID_Employee', 'Name_Employee', 'Annual_Income']
    print(df)

def Query4_info_hr():
    print('TASK: Find all the email, name and surname HR who have a phone benefit of the brand "Samsung" and their annual salary is beyond the 25 k treshold. Order the result by descendent Annual Salary.\n')

def Query5_hr():
    print('RESULT OF THE HUMAN RESOURCES QUERY 5:  ')
    Query5_info_hr()
    
    string = 'SELECT temp1."ID_Human_Resources", temp1.count_employee_hired as "#Employee_Hired", employee."Name_Employee", employee."Surname_Employee", employee."Level_Employee"\
              FROM (\
                        SELECT empl."ID_Human_Resources", COUNT(empl."ID_Human_Resources") as count_employee_hired\
                        FROM public."EMPLOYEE" as empl\
                        GROUP BY empl."ID_Human_Resources"\
		) as temp1	\
	        INNER JOIN public."EMPLOYEE" as employee ON temp1."ID_Human_Resources" = employee."ID_Employee"\
              ORDER BY temp1.count_employee_hired DESC'
    cur.execute(string)
    df = pd.DataFrame(cur.fetchall())
    df.columns = ['ID_Human_Resources', '#Employee_Hired', 'Name_Employee', 'Surname_Employee', 'Level_Employee']
    print(df)

def Query5_info_hr():
    print('TASK: Find the ranking of the HR basing on how many employee they have hired specifying their name and surname, ordering in descending order w.r.t. the number of employee hired..\n')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def help():
    print('\nHELPDESK BASIC APPLICATION v_0.1')
    print('\n• Press "NumberQuery.info" in order to see the text of the Query')


try:
    with psycopg2.connect( host = hostname, dbname = database, user = username, password = pwd, port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            if __name__=='__main__':
                    
                logged = False      #Used to see whether you are logged or not
                check = False       
                lead = False        #Used to verify whether you were entered with a Leadership Account.
                
                while(True):
                    option = ''
                    if not logged:
                        usr = input('\nEnter your Employee Account: ')
                        pswd = getpass.getpass('Password: ')
                        query_id_employee = 'SELECT "ID_Employee" FROM "EMPLOYEE" WHERE "Username_Employee" = ' + "'" + '%s' % usr + "' and " + '"Password_Employee" = ' + "'" +  '%s' % pswd +  "'"
                        checkUsername = cur.execute(query_id_employee)
                        df = pd.DataFrame(cur.fetchall())
                        df.columns = ['ID_Employee']       
                        Id = df['ID_Employee'][0][1:7]        #Take the Constant Part that could be only: IDWT1, IDWT2
                        if Id == '':
                            print('\nEmployee Not Recognized')
                        else:
                            logged = True
                            #Check what type of Employee is:
                            type_employee = ''
                            
                            if Id[:5] == 'IDWT1':
                                type_employee = '1_st_Level_Technician'
                                print("\nEmployee Logged! You are a 1_st_Level_Technician! Welcome Back to your HelpDesk's portal!")
                            elif Id[:5] == 'IDWT2':
                                type_employee = '2_nd_Level_Technician'
                                print("\nEmployee Logged! You are a 2_st_Level_Technician! Welcome Back to your HelpDesk's portal!")
                            elif Id[:5] == 'IDWAM':
                                type_employee = 'Account_Manager'
                                print("\nEmployee Logged! You are an Account_Manager! Welcome Back to your HelpDesk's portal!")
                            elif Id[:5] == 'IDWBM':
                                type_employee = 'Business_Manager'
                                print("\nEmployee Logged! You are a Business_Manager! Welcome Back to your HelpDesk's portal!")
                            elif Id[:5] == 'IDWHR':
                                type_employee = 'Human_Resourcer'
                                print("\nEmployee Logged! You are a Human_Resourcer! Welcome Back to your HelpDesk's portal!")
                            elif Id[:6] == 'IDWFIN':            
                                type_employee = 'Financer'
                                print("\nEmployee Logged! You are a Financer! Welcome Back to your HelpDesk's portal!")
                            elif Id[:3] == 'IDL':               
                                type_employee = 'Leadership_Employee'
                                lead = True
                                print("\nEmployee Logged! You are a Leadership_Employee! Welcome Back to your HelpDesk's portal!")
                    
                    else:
                        option = input('\nDo you want to continue(Y/N)? ')
                        if option == 'C' or option == 'c' or option == 'Y' or option == 'y' or not option:  #Pythonic: press also enter!!!
                            query_id_employee = 'SELECT "ID_Employee" FROM "EMPLOYEE" WHERE "Username_Employee" = ' + "'" + '%s' % usr + "' and " + '"Password_Employee" = ' + "'" +  '%s' % pswd +  "'"
                            checkUsername = cur.execute(query_id_employee)
                            df = pd.DataFrame(cur.fetchall())
                            df.columns = ['ID_Employee']
                
                            
                            #Different Thing to Do, depending on the Employee Type:
                            if type_employee == '1_st_Level_Technician':
                                print_menu_tech1()
                            elif type_employee == '2_nd_Level_Technician':
                                print_menu_tech2()
                            elif type_employee == 'Account_Manager':
                                print_menu_account_manager()
                            elif type_employee == 'Business_Manager':
                                print_menu_business_manager()
                            elif type_employee == 'Financer':
                                print_menu_finance()
                            elif type_employee == 'Human_Resourcer':
                                print_menu_hr()
                            elif type_employee == 'Leadership_Employee':
                                print_menu_lead()
                            option = input('\nEnter your choice: ')
                            
                        elif option == 'N' or option == 'n' or option == 'E' or option == 'e' :
                            print('Thanks for having used the HelpDesk Database Application')
                            exit()
                                
                    
                    #Different Thing to Do, depending on the Employee Type:
                    
                    #1_ST_LEVEL_TECHINCIAN: 
                    if option == '1' and (type_employee == '1_st_Level_Technician'):
                        Query1_tech1()
                    elif option == '1.info' and (type_employee == '1_st_Level_Technician'):
                        Query1_info_tech1()
                    elif option == '2' and (type_employee == '1_st_Level_Technician'):
                        Query2_tech1()
                    elif option == '2.info' and (type_employee == '1_st_Level_Technician'):
                        Query2_info_tech1()
                    elif option == '3' and (type_employee == '1_st_Level_Technician'):
                        Query3_tech1()
                    elif option == '3.info' and (type_employee == '1_st_Level_Technician'):
                        Query3_info_tech1()
                    elif option == '4' and (type_employee == '1_st_Level_Technician'):
                        Query4_tech1()
                    elif option == '4.info' and (type_employee == '1_st_Level_Technician'):
                        Query4_info_tech1()
                    elif option == '5' and (type_employee == '1_st_Level_Technician'):
                        Query5_tech1()
                    elif option == '5.info' and (type_employee == '1_st_Level_Technician'):
                        Query5_info_tech1()
                    
                    elif (option == 'Q' or option == 'q') and (type_employee == '1_st_Level_Technician'): 
                            print('Thanks for having used the HelpDesk Database Application')
                            exit()
                    elif (option == 'H' or option == 'h') and (type_employee == '1_st_Level_Technician'):
                            help()
                            logged = False
                    elif (option == 'B' or option == 'b') and (type_employee == '1_st_Level_Technician'): 
                            print('Going back to the Login Part')
                            logged = False
                           
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == '1_st_Level_Technician') and lead == True: 
                            type_employee = 'Leadership_Employee'
                            print('Going back to the Leadership Working Area')
                    elif (option == 'L' or option == 'l'or option == 'lead') and (type_employee == '1_st_Level_Technician') and lead == False: 
                            print('You DO NOT have the Permissions to go to the Leadership Working Area')
                            
                    
                    elif check == False and type_employee == '1_st_Level_Technician':
                            check = True      
                    elif type_employee == '1_st_Level_Technician' and option != 'L' and option != 'l':   
                            print('Invalid Option. Please enter a number between 1 and 5.')
                
                           
                    #2_ND_LEVEL_TECHINCIAN: 
                    if option == '1' and (type_employee == '2_nd_Level_Technician'):
                        Query1_tech2()
                    elif option == '1.info' and (type_employee == '2_nd_Level_Technician'):
                        Query1_info_tech2()
                    elif option == '2' and (type_employee == '2_nd_Level_Technician'):
                        Query2_tech2()
                    elif option == '2.info' and (type_employee == '2_nd_Level_Technician'):
                        Query2_info_tech2()
                    elif option == '3' and (type_employee == '2_nd_Level_Technician'):
                        Query3_tech2()
                    elif option == '3.info' and (type_employee == '2_nd_Level_Technician'):
                        Query3_info_tech2()
                    elif option == '4' and (type_employee == '2_nd_Level_Technician'):
                        Query4_tech2()
                    elif option == '4.info' and (type_employee == '2_nd_Level_Technician'):
                        Query4_info_tech2()
                    elif option == '5' and (type_employee == '2_nd_Level_Technician'):
                        Query5_tech2()
                    elif option == '5.info' and (type_employee == '2_nd_Level_Technician'):
                        Query5_info_tech2()
                    
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == '2_nd_Level_Technician') and lead == True: 
                            type_employee = 'Leadership_Employee'
                            print('Going back to the Leadership Working Area')
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == '2_nd_Level_Technician') and lead == False: 
                            print('You DO NOT have the Permissions to go to the Leadership Working Area')
                    
                    elif (option == 'Q' or option == 'q') and (type_employee == '2_nd_Level_Technician'): 
                            print('Thanks for having used the HelpDesk Database Application')
                            exit()
                    elif (option == 'H' or option == 'h') and (type_employee == '2_nd_Level_Technician'):
                            help()
                    elif (option == 'B' or option == 'b') and (type_employee == '2_nd_Level_Technician'): 
                            print('Going back to the Login Part')
                            logged = False
                    elif check == False and type_employee == '2_nd_Level_Technician':
                            check = True      
                    elif type_employee == '2_nd_Level_Technician' and option != 'L' and option != 'l':   
                            print('Invalid Option. Please enter a number between 1 and 5.')
                
                            
                    #ACCOUNT_MANAGER: 
                    if option == '1' and (type_employee == 'Account_Manager'):
                        Query1_managera()
                    elif option == '1.info' and (type_employee == 'Account_Manager'):
                        Query1_info_managera()
                    elif option == '2' and (type_employee == 'Account_Manager'):
                        Query2_managera()
                    elif option == '2.info' and (type_employee == 'Account_Manager'):
                        Query2_info_managera()
                    elif option == '3' and (type_employee == 'Account_Manager'):
                        Query3_managera()
                    elif option == '3.info' and (type_employee == 'Account_Manager'):
                        Query3_info_managera()
                    elif option == '4' and (type_employee == 'Account_Manager'):
                        Query4_managera()
                    elif option == '4.info' and (type_employee == 'Account_Manager'):
                        Query4_info_managera()
                    elif option == '5' and (type_employee == 'Account_Manager'):
                        Query5_managera()
                    elif option == '5.info' and (type_employee == 'Account_Manager'):
                        Query5_info_managera()
                    
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == 'Account_Manager') and lead == True: 
                            type_employee = 'Leadership_Employee'
                            print('Going back to the Leadership Working Area')
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == 'Account_Manager') and lead == False: 
                            print('You DO NOT have the Permissions to go to the Leadership Working Area')
                    
                    elif (option == 'Q' or option == 'q') and (type_employee == 'Account_Manager'): 
                            print('Thanks for having used the HelpDesk Database Application')
                            exit()
                    elif (option == 'H' or option == 'h') and (type_employee == 'Account_Manager'):
                            help()  
                    elif (option == 'B' or option == 'b') and (type_employee == 'Account_Manager'): 
                            print('Going back to the Login Part')
                            logged = False
                    elif check == False and type_employee == 'Account_Manager':
                            check = True      
                    elif type_employee == 'Account_Manager' and option != 'L' and option != 'l':   
                            print('Invalid Option. Please enter a number between 1 and 5.')
                            
                    #BUSINESS_MANAGER: 
                    if option == '1' and (type_employee == 'Business_Manager'):
                        Query1_managerb()
                    elif option == '1.info' and (type_employee == 'Business_Manager'):
                        Query1_info_managerb()
                    elif option == '2' and (type_employee == 'Business_Manager'):
                        Query2_managerb()
                    elif option == '2.info' and (type_employee == 'Business_Manager'):
                        Query2_info_managerb()
                    elif option == '3' and (type_employee == 'Business_Manager'):
                        Query3_managerb()
                    elif option == '3.info' and (type_employee == 'Business_Manager'):
                        Query3_info_managerb()
                    elif option == '4' and (type_employee == 'Business_Manager'):
                        Query4_managerb()
                    elif option == '4.info' and (type_employee == 'Business_Manager'):
                        Query4_info_managerb()
                    elif option == '5' and (type_employee == 'Business_Manager'):
                        Query5_managerb()
                    elif option == '5.info' and (type_employee == 'Business_Manager'):
                        Query5_info_managerb()
                    
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == 'Business_Manager') and lead == True: 
                            type_employee = 'Leadership_Employee'
                            print('Going back to the Leadership Working Area')
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == 'Business_Manager') and lead == False: 
                            print('You DO NOT have the Permissions to go to the Leadership Working Area')
                            
                    elif (option == 'Q' or option == 'q') and (type_employee == 'Business_Manager'): 
                            print('Thanks for having used the HelpDesk Database Application')
                            exit()
                    elif (option == 'H' or option == 'h') and (type_employee == 'Business_Manager'):
                            help()
                    elif (option == 'B' or option == 'b') and (type_employee == 'Business_Manager'): 
                            print('Going back to the Login Part')
                            logged = False
                    elif check == False and type_employee == 'Account_Manager':
                            check = True      
                    elif type_employee == 'Business_Manager' and option != 'L' and option != 'l':   
                            print('Invalid Option. Please enter a number between 1 and 5.')
                            
                    #HUMAN_RESOURCES: 
                    if option == '1' and (type_employee == 'Human_Resourcer'):
                        Query1_hr()
                    elif option == '1.info' and (type_employee == 'Human_Resourcer'):
                        Query1_info_hr()
                    elif option == '2' and (type_employee == 'Human_Resourcer'):
                        Query2_hr()
                    elif option == '2.info' and (type_employee == 'Human_Resourcer'):
                        Query2_info_hr()
                    elif option == '3' and (type_employee == 'Human_Resourcer'):
                        Query3_hr()
                    elif option == '3.info' and (type_employee == 'Human_Resourcer'):
                        Query3_info_hr()
                    elif option == '4' and (type_employee == 'Human_Resourcer'):
                        Query4_hr()
                    elif option == '4.info' and (type_employee == 'Human_Resourcer'):
                        Query4_info_hr()
                    elif option == '5' and (type_employee == 'Human_Resourcer'):
                        Query5_hr()
                    elif option == '5.info' and (type_employee == 'Human_Resourcer'):
                        Query5_info_hr()
                    
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == 'Human_Resourcer') and lead == True: 
                            type_employee = 'Leadership_Employee'
                            print('Going back to the Leadership Working Area')
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == 'Human_Resourcer') and lead == False: 
                            print('You DO NOT have the Permissions to go to the Leadership Working Area')
                            
                    elif (option == 'Q' or option == 'q') and (type_employee == 'Human_Resourcer'): 
                            print('Thanks for having used the HelpDesk Database Application')
                            exit()
                    elif (option == 'H' or option == 'h') and (type_employee == 'Human_Resourcer'):
                            help()
                    elif (option == 'B' or option == 'b') and (type_employee == 'Human_Resourcer'): 
                            print('Going back to the Login Part')
                            logged = False
                    elif check == False and type_employee == 'Human_Resourcer':
                            check = True      
                    elif type_employee == 'Human_Resourcer' and option != 'L' and option != 'l':   
                            print('Invalid Option. Please enter a number between 1 and 5.')
                            
                    #FINANCE: 
                    if option == '1' and (type_employee == 'Financer'):
                        Query1_Finance()
                    elif option == '1.info' and (type_employee == 'Financer'):
                        Query1_info_Finance()
                    elif option == '2' and (type_employee == 'Financer'):
                        Query2_Finance()
                    elif option == '2.info' and (type_employee == 'Financer'):
                        Query2_info_Finance()
                    elif option == '3' and (type_employee == 'Financer'):
                        Query3_Finance()
                    elif option == '3.info' and (type_employee == 'Financer'):
                        Query3_info_Finance()
                    elif option == '4' and (type_employee == 'Financer'):
                        Query4_Finance()
                    elif option == '4.info' and (type_employee == 'Financer'):
                        Query4_info_Finance()
                    elif option == '5' and (type_employee == 'Financer'):
                        Query5_Finance()
                    elif option == '5.info' and (type_employee == 'Financer'):
                        Query5_info_Finance()
                    
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == 'Financer') and lead == True: 
                            type_employee = 'Leadership_Employee'
                            print('Going back to the Leadership Working Area')
                    elif (option == 'L' or option == 'l' or option == 'lead') and (type_employee == 'Financer') and lead == False: 
                            print('You DO NOT have the Permissions to go to the Leadership Working Area')
                            
                    elif (option == 'Q' or option == 'q') and (type_employee == 'Financer'): 
                            print('Thanks for having used the HelpDesk Database Application')
                            exit()
                    elif (option == 'H' or option == 'h') and (type_employee == 'Financer'):
                            help()
                    elif (option == 'B' or option == 'b') and (type_employee == 'Financer'): 
                            print('Going back to the Login Part')
                            logged = False
                    elif check == False and type_employee == 'Financer':
                            check = True      
                    elif type_employee == 'Financer' and option != 'L' and option != 'l':   
                            print('Invalid Option. Please enter a number between 1 and 5.')
                        
                    #LEADERSHIP:   
                    if option == '1' and (type_employee == 'Leadership_Employee'):
                            Query1_Lead()
                    elif option == '1.info' and (type_employee == 'Leadership_Employee'):
                            Query1_info_Lead()
                    elif option == '2' and (type_employee == 'Leadership_Employee'):
                            Query2_Lead()
                    elif option == '2.info' and (type_employee == 'Leadership_Employee'):
                            Query2_info_Lead()
                    elif option == '3' and (type_employee == 'Leadership_Employee'):
                            Query3_Lead()
                    elif option == '3.info' and (type_employee == 'Leadership_Employee'):
                            Query3_info_Lead()
                    elif option == '4' and (type_employee == 'Leadership_Employee'):
                            Query4_Lead()
                    elif option == '4.info' and (type_employee == 'Leadership_Employee'):
                            Query4_info_Lead()
                    elif option == '5' and (type_employee == 'Leadership_Employee'):
                            Query5_Lead()
                    elif option == '5.info' and (type_employee == 'Leadership_Employee'): 
                            Query5_info_Lead()
                    elif option == '6' and (type_employee == 'Leadership_Employee'):
                            Query6_Lead()
                    elif option == '6.info' and (type_employee == 'Leadership_Employee'): 
                            Query6_info_Lead()
                    elif option == '7' and (type_employee == 'Leadership_Employee'):
                            Query7_Lead()
                    elif option == '7.info' and (type_employee == 'Leadership_Employee'): 
                            Query7_info_Lead()
                    elif option == '8' and (type_employee == 'Leadership_Employee'):
                            Query8_Lead()
                    elif option == '8.info' and (type_employee == 'Leadership_Employee'): 
                            Query8_info_Lead()
                    elif (option == 'Tech1' or option == 'tech1' or option == 't1') and (type_employee == 'Leadership_Employee'): 
                            type_employee = '1_st_Level_Technician'
                    elif (option == 'Tech2' or option == 'tech2' or option == 't2') and (type_employee == 'Leadership_Employee'): 
                            type_employee = '2_nd_Level_Technician'
                    elif (option == 'hr' or option == 'HR' or option == 'Human Resources') and (type_employee == 'Leadership_Employee'): 
                            type_employee = 'Human_Resourcer'
                    elif (option == 'am' or option == 'managera' or option == 'MANAGERA' or option == 'AM' or option == 'Account Manager') and (type_employee == 'Leadership_Employee'): 
                            type_employee = 'Account_Manager'
                    elif (option == 'bm' or option == 'managerb' or option == 'MANAGERB' or option == 'BM' or option == 'Business Manager') and (type_employee == 'Leadership_Employee'): 
                            type_employee = 'Business_Manager'
                    elif (option == 'Finance' or option == 'finance' or option == 'f') and (type_employee == 'Leadership_Employee'): 
                            type_employee = 'Financer'
                    
                    elif (option == 'Q' or option == 'q') and (type_employee == 'Leadership_Employee'): 
                            print('Thanks for having used the HelpDesk Database Application')
                            exit()
                    elif (option == 'H' or option == 'h') and (type_employee == 'Leadership_Employee'):
                            help()
                    elif (option == 'B' or option == 'b') and (type_employee == 'Leadership_Employee'): 
                            print('Going back to the Login Part')
                            logged = False
                    elif check == False and type_employee == 'Leadership_Employee':
                            check = True      
                    elif type_employee == 'Leadership_Employee' and option != 'L' and option != 'l':   
                            print('Invalid Option. Please enter a number between 1 and 8.')
                            
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()