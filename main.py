from components.import_data_v1 import import_data
from components.clean_data_v1 import filter_and_clean_data



def main():
    print("\nStarting the module")
    import_data()
    filter_and_clean_data()

    print("The module run is completed")






if __name__ == "__main__":
    main()