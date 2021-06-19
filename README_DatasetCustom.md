# DATASET_CUSTOMIZING  

### NOTES
For easier customization, recommended is module.  
For every function you must also pass in the dataset you want to modify.  
It does not matter what case you type in your column names etc., it takes any case lower/upper/mixed, no need to bother with the right case.  

If using input:  
Customization is based on your input, read carefully what the program wants from you.  
!!! If you run into any error rerun the program and use it all over again !!!  


If using module:  
read_file --> rather use pandas for reading :)  
change_col_names --> change column names, takes dict where key is the original name (case doesn't matter), and value is the renamed column.  
drop_columns_rows --> drop column (no matter the lower or upper case you name them), or some range of rows.  
drop_replace_na --> drop NaN values or values you name in other_than_na parameter, and you can also replace them with something in replace_na_with parameter.  
change_number_format --> specific case, when you have all float numbers as 1,2 instead of 1.2 --> changes 1,2 into 1.2, just type column names (no matter in what lower/upper case)  
handle_non_numeric --> when you have categorical columns, it will replace the categories into unique int numbers f.e. Man/Woman --> 0/1, just pass column names you want to handle non numeric values in    
balance --> when want to have balanced data, when you have want to have the same amount of men as women f.e., you just specify the column name in balance_by parameter, by what you want to balance your dataset  
