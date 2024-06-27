import os, shutil, scripts.constants


class Program:
    def __init__(self) -> None:
        pass 

    def delete_folders(self) -> None:
        """
        Delete the folders of the content directory.


            Parameters
                None

            Returns
                return None
        """

        for item in os.listdir(scripts.constants.content_folder_path):
            item_path = os.path.join(scripts.constants.content_folder_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)