import re

def create_transactional_matrix(dataset):

    with open(f"{dataset}.txt", 'r') as f:
        given_data = f.read()
        entire_items = (re.split(",|\n", given_data))
        unique_items = set(entire_items)
        # print(f"Unique unique_items: {unique_items}, \n Length: {len(unique_items)}")
        
        ''' Array of all transactions '''
        all_transactions = list(re.split("\n", given_data))

    # print(unique_items)
    # print(len(unique_items))

    ''' Create a new transactional_matrix.txt file '''
    with open('transactional_matrix.txt', 'w') as f:
        #Header of unique items
        f.write((','.join(item for item in unique_items)))
        f.write('\n')

        # If an item is found in a transaction, allocate 1 to the cell. Otherwise, 0.
        for transaction in all_transactions:
            arr = []
            for item_name in unique_items:  
                if item_name in transaction:
                    arr.append(1)
                else:
                    arr.append(0)
            f.write((','.join(str(item) for item in arr)) ) 
            f.write('\n')

if __name__ == "__main__":
    dataset = input('Enter the name of the dataset txt file (eg: grocery_dataset):')
    print('The output file is created as transactional_matrix.txt')
    create_transactional_matrix(dataset)