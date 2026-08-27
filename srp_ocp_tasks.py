from abc import ABC, abstractmethod


# --- SRP: Single Responsibility Principle ---
class Task:

    def __init__(self, task_id, description, due_date=None, completed=False, priority="medium"):
        self.id = task_id
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.priority = priority  # เพิ่ม attribute priority

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else " "
        due = f" (Due: {self.due_date})" if self.due_date else ""
        return f"[{status}] {self.id}. {self.description}{due} [Priority: {self.priority}]"


# Interface สำหรับบันทึกข้อมูล (OCP & DIP)
class TaskStorage(ABC):

    @abstractmethod
    def save(self, tasks):
        pass


class FileTaskStorage(TaskStorage):

    def __init__(self, filename="tasks_solid.txt"):
        self.filename = filename

    def save(self, tasks):
        with open(self.filename, "w") as f:
            for task in tasks:
                f.write(
                    f"{task.id},{task.description},{task.due_date},{task.completed},{task.priority}\n"
                )
        print(f"Tasks saved to file: {self.filename}")


# --- OCP: Open/Closed Principle ---
# คลาสแสดงผลแบบปกติ
class TaskPresenter:

    def display(self, tasks):
        print("\n--- Current Tasks ---")
        if not tasks:
            print("No tasks available.")
            return
        for task in tasks:
            print(task)
        print("--------------------")


# คลาสแสดงผลแบบเน้นข้อความ (ขยายเพิ่มโดยไม่แก้คลาสเดิม)
class DetailedTaskPresenter(TaskPresenter):

    def display(self, tasks):
        print("\n================ DETAILED TASK LIST ================")
        if not tasks:
            print("No tasks available in the system.")
            return
        for task in tasks:
            status_text = "COMPLETED" if task.completed else "PENDING"
            print(
                f"ID: {task.id} | Status: {status_text} | Task: {task.description} | Due: {task.due_date} | Priority: {task.priority}"
            )
        print("====================================================")


# คลาสหลักสำหรับจัดการงาน (ไม่ขึ้นกับไฟล์หรือการแสดงผลโดยตรง)
class TaskManager:

    def __init__(self, storage: TaskStorage, presenter: TaskPresenter):
        self.tasks = []
        self.next_id = 1
        self.storage = storage
        self.presenter = presenter

    def add_task(self, description, due_date=None, priority="medium"):
        task = Task(self.next_id, description, due_date, priority=priority)
        self.tasks.append(task)
        self.next_id += 1
        print(f"Task '{description}' added.")
        return task

    def mark_task_completed(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.mark_completed()
                print(f"Task {task_id} marked as completed.")
                return True
        print(f"Task {task_id} not found.")
        return False

    def show_tasks(self):
        self.presenter.display(self.tasks)

    def save_tasks(self):
        self.storage.save(self.tasks)


if __name__ == "__main__":
    storage = FileTaskStorage()
    presenter = DetailedTaskPresenter()

    manager = TaskManager(storage, presenter)
    manager.add_task("Learn SOLID Principles", "2024-08-10", priority="high")
    manager.add_task("Refactor Code", "2024-08-15", priority="medium")

    manager.show_tasks()
    manager.mark_task_completed(1)
    manager.show_tasks()
    manager.save_tasks()