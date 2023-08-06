import torchvision.datasets as datasets
import torchvision.datasets.folder as datafolder
import os

"""
DatasetFolder/ImageFolder based classes
original DatasetFolder/ImageFolder documentation: https://pytorch.org/docs/stable/_modules/torchvision/datasets/folder.html
github: https://github.com/pytorch/vision/blob/master/torchvision/datasets/folder.py
In this module, the original DatasetFolder/ImageFolder was overwritten and now it will load image pairs(corresponding) rather than single images.
"""

class DatasetFolder(datasets.VisionDataset):        
    # class DatasetFolder would be wrapped by the class ImageFolder, so you should call ImageFolder instead
    # root1 -> path of your imagefolder1; root2 -> path of your imagefolder2
    def __init__(self, root1, root2, loader, extensions=None, transform=None,
                 target_transform=None, is_valid_file=None): 
        # For consistency, give root1 to the parent class constructor   
        super(DatasetFolder, self).__init__(root = root1, transform=transform,
                                            target_transform=target_transform)
        self.root1 = root1
        self.root2 = root2
        classes1, class_to_idx1 = self._find_classes(self.root1)
        classes2, class_to_idx2 = self._find_classes(self.root2)
        samples1 = datafolder.make_dataset(self.root1, class_to_idx1, extensions, is_valid_file)
        samples2 = datafolder.make_dataset(self.root2, class_to_idx2, extensions, is_valid_file)

        if len(samples1) == 0:
            msg = "Found 0 files in subfolders of: {}\n".format(self.root1)
            if extensions is not None:
                msg += "Supported extensions are: {}".format(",".join(extensions))
            raise RuntimeError(msg)
        if len(samples2) == 0:
            msg = "Found 0 files in subfolders of: {}\n".format(self.root2)
            if extensions is not None:
                msg += "Supported extensions are: {}".format(",".join(extensions))
            raise RuntimeError(msg)

        self.loader = loader
        self.extensions = extensions

        self.classes1 = classes1
        self.classes2 = classes2
        self.class_to_idx1 = class_to_idx1
        self.class_to_idx2 = class_to_idx2
        self.samples1 = samples1
        self.samples2 = samples2
        self.targets1 = [s[1] for s in samples1]
        self.targets2 = [s[1] for s in samples2]
      
    def _find_classes(self, dir):
        """
        Finds the class folders in a dataset.

        Args:
            dir (string): Root directory path.

        Returns:
            tuple: (classes, class_to_idx) where classes are relative to (dir), and class_to_idx is a dictionary.

        Ensures:
            No class is a subdirectory of another.
        """
        classes = [d.name for d in os.scandir(dir) if d.is_dir()]
        classes.sort()
        class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}
        return classes, class_to_idx
    
    # redefine the __getitem__ method for bivariate iteration
    def __getitem__(self, index):
        """
        Args:
            index1 (int), index2 (int): Index1, Index2

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        """
        path1, target1 = self.samples1[index]
        path2, target2 = self.samples2[index]

        sample1 = self.loader(path1)
        sample2 = self.loader(path2)

        if self.transform is not None:
            sample1 = self.transform(sample1)
            sample2 = self.transform(sample2)

        if self.target_transform is not None:
            target1 = self.target_transform(target1)
            target2 = self.target_transform(target2)

        return sample1, target1, sample2, target2

    def __len__(self):
        #len of samples1 == len of samples2
        return len(self.samples1)   

class ImageFolder(DatasetFolder):
    """A generic data loader where the images are arranged in this way: ::

        root1/dog/xxx.png
        root1/dog/xxy.png
        root1/dog/xxz.png

        root1/cat/123.png
        root1/cat/nsdf3.png
        root1/cat/asd932_.png


        root2/dog/xxx.png
        root2/dog/xxy.png
        root2/dog/xxz.png

        root2/cat/123.png
        root2/cat/nsdf3.png
        root2/cat/asd932_.png

    Args:
        root1 (string): Root1 directory path.
        root2 (string): Root2 directory path.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        loader (callable, optional): A function to load an image given its path.
        is_valid_file (callable, optional): A function that takes path of an Image file
            and check if the file is a valid file (used to check of corrupt files)

     Attributes:
        classes1 (list): List of the class1 names sorted alphabetically.
        classes2 (list): List of the class2 names sorted alphabetically.
        class_to_idx1 (dict): Dict with items (class_name1, class_index1).
        class_to_idx2 (dict): Dict with items (class_name2, class_index2).
        imgs1 (list): List of (image path1, class_index1) tuples
        imgs2 (list): List of (image path2, class_index2) tuples
    """

    def __init__(self, root1, root2, transform=None, target_transform=None,
                 loader=datafolder.default_loader, is_valid_file=None):
        super(ImageFolder, self).__init__(root1, root2, loader, datafolder.IMG_EXTENSIONS if is_valid_file is None else None,
                                          transform=transform,
                                          target_transform=target_transform,
                                          is_valid_file=is_valid_file)
        self.imgs1 = self.samples1
        self.imgs2 = self.samples2
