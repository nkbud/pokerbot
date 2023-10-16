

from lookup import LookupTable

if __name__ == "__main__":
    table = LookupTable()
    table.write_table_to_disk(table.flush_lookup, "./flushes.csv")
    table.write_table_to_disk(table.unsuited_lookup, "./multiples.csv")