from UseCases.FileExecute.FileHandler import FileHandler
from UseCases.store.File_Repo import InMemoryFileRepository
from UseCases.OsSystemCall.SystemCall_Factory import SystemCallFactory, OS_Type


if __name__ == "__main__":
    file_repository = InMemoryFileRepository([])
    os_system_call = SystemCallFactory().create_by_type(OS_Type.WINDOWS)
    file_handler = FileHandler(file_repository, os_system_call)
    file_handler.GetFilesByType(r"C:\Users\hoang\Desktop\LazyTool", r".*")
    print(file_repository)   