def show():
    # Shows menu for classifying gesture data
    done = False

    while done is False:
        print("-------------------")
        print("DATA CLASSIFICATION")
        print("-------------------")

        # First - Show files available for classification (pickle files)
        # Second - Show feature type and kernel type based on chosen pickle file
        # Third - Call Data Classifier function
