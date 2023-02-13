import create_database
import schedule, time_data

def run():
    # DELETE DATABSE BEFORE CREATE
    create_database.multi_delete_table()
    # CREATE DATABSE BEFORE SCHEDULE (immediately)
    create_database.multi_get()

    # schedule
    schedule.every(5).minutes.do(create_database.multi_get)
    schedule.every(1).days.do(create_database.multi_upload)

    # schedule test
    # schedule.every(5).seconds.do(create_database.multi_get)
    # schedule.every(30).seconds.do(create_database.multi_upload)

    while True:
        schedule.run_pending()
        time_data.sleep(1)


if __name__ == "__main__":

    run()

