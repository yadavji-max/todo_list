from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='defaut_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        # return self.task  # normal
        return f"{self.task}. {self.deadline.strftime('%d')} {self.deadline.strftime('%b')}"  # all tasl


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def Todays_task(session):
    print(f'Today {datetime.today().day} {datetime.today().strftime("%b")}:')
    rows = session.query(Table).filter(Table.deadline == datetime.today().strftime("%Y-%m-%d")).order_by(Table.id).all()
    if len(rows) != 0:
        for i, row in enumerate(rows):
            print(f'{i + 1}. {row}')
    else:
        print("Nothing to do!")


def Weeks_task(session):
    for i in range(7):
        rows = session.query(Table).filter(
            Table.deadline == (datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d')).all()
        if len(rows) != 0:
            print(
                f'{(datetime.today() + timedelta(days=i)).strftime("%A")} {(datetime.today() + timedelta(days=i)).day} {(datetime.today() + timedelta(days=i)).strftime("%b")}:')
            for i, row in enumerate(rows):
                print(f'{i + 1}. {row}')
        else:
            print(
                f'{(datetime.today() + timedelta(days=i)).strftime("%A")} {(datetime.today() + timedelta(days=i)).day} {(datetime.today() + timedelta(days=i)).strftime("%b")}:')
            print("Nothing to do!")
        print("")


def All_tasks(session):
    rows = session.query(Table).order_by(Table.deadline).all()
    print("All task:")
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for i, row in enumerate(rows):
            print(f'{i + 1}. {row}')


def Add_task(task_, deadline_, session):
    new_row = Table(task=task_,
                    deadline=datetime.strptime(deadline_, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()


def Missed_tasks(session):
    rows = session.query(Table).filter(Table.deadline < datetime.today().strftime("%Y-%m-%d")).all()
    if len(rows) != 0:
        for row in rows:
            print(row)
    else:
        print("Nothing is missed!")
    print("")



def Delete_task(session):
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing to delete!")
    else:
        print("Choose the number of the task you want to delete:")
        for i, row in enumerate(rows):
            print(f'{i + 1}. {row}')

    n = int(input())

    for i, row in enumerate(rows):
        if (i + 1) == n:
            session.delete(row)
            session.commit()
    print("The task has been deleted!")


def todo():
    while (True):

        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

        menu_input = int(input())

        if menu_input == 1:
            Todays_task(session)

        elif menu_input == 2:
            Weeks_task(session)

        elif menu_input == 3:
            All_tasks(session)

        elif menu_input == 4:
            Missed_tasks(session)

        elif menu_input == 6:
            Delete_task(session)

        elif menu_input == 5:
            print("Enter task")
            t = input()
            print("Enter deadline")
            d = input()
            Add_task(t, d, session)

        elif menu_input == 0:
            print("Bye!")
            break


todo()
