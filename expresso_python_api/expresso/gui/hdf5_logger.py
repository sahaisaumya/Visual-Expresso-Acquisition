import h5py
import time
import datetime

class HDF5_Logger(object):
    """
    Simple HDF5 data logger class
    """

    def __init__(self,filename,mode='w'):
        self.filename = filename
        self.data_size = {}
        self.resize_incr = 1000
        self.date_format = '%m-%d-%Y %H:%M:%S'
        self.f = h5py.File(self.filename,mode)

    def __del__(self):
        """
        Resizes datasets in hdf5 file to reflect the final sizes.
        """
        for name, size in self.data_size.iteritems():
            dataset = self.f[name]
            elem_shape = dataset.shape[1:]
            new_shape = (size,) + elem_shape
            dataset.resize(new_shape)
        self.f.close()

    def list(self,pathname):
        return list(self.f[pathname])

    def add_attribute(self,pathname,name,value):
        """
        Add attribute to log element - either group of dataset 
        """
        pathname = self._get_full_pathname(pathname)
        self.f[pathname].attrs[name] = value

    def add_datetime(self,pathname, name='datetime'):
        """
        Add datetime attribute to log element (group or dataset) specified
        by the pathname
        """
        date_string = datetime.datetime.now().strftime(self.date_format)
        self.add_attribute(pathname, name, date_string)

    def add_group(self,pathname,create=True):
        """
        Add a group to the hdf5 log. 

        pathname = path to group in hdf5 log. Note, pathname can be of two
        forms: a simple string without a '/' or a path string such as
        '/level1/level2/newgroup'.   
        """
        subgroup, name = self._split_pathname(pathname,create=create)
        subgroup.create_group(name)

    def add_dataset(self,pathname,elem_shape,dtype='f',create=True):
        """
        Adds dataset to hdf5 log file.
        """
        subgroup, name = self._split_pathname(pathname,create=create)
        inishape = (self.resize_incr,) + elem_shape
        maxshape = (None,) + elem_shape
        dataset = subgroup.create_dataset(name, inishape, dtype, maxshape=maxshape)
        self.data_size[dataset.name] = 0

    def add_dataset_value(self,pathname,value):
        """
        Adds value to log dataset.  
        """
        pathname = self._get_full_pathname(pathname)
        dataset = self.f[pathname]

        # Resize dataset if required
        n = self.data_size[pathname]
        space_available = dataset.shape[0]
        if n >= space_available:
            elem_shape = dataset.shape[1:]
            new_shape = (n+self.resize_incr,) + elem_shape
            dataset.resize(new_shape)

        # Add item to dataset
        dataset[n]= value
        self.data_size[pathname] = n+1

    def _split_pathname(self,pathname,create=True):
        """
        Gets the subgroup and name of the item specified via the
        pathnmae
        """
        pathlist = pathname.split('/')
        if len(pathlist) == 1:
            name = pathname
            subgroup = self.f
        else:
            path = pathlist[1:-1]
            name = pathlist[-1]
            subgroup = self._get_subgroup(path,create=create)
        return subgroup, name

    def _get_subgroup(self,pathlist,create=True):
        """
        Get subgroup specified by pathlist. Create intermediate subgroups
        if they don't already exist.
        """
        subgroup = self.f
        for item in pathlist:
            try:
                subgroup = subgroup[item]
            except KeyError, e:
                if create:
                    subgroup.create_group(item)
                    subgroup = subgroup[item]
                else:
                    pathstr = '/'.join(path)
                    pathstr = '/' + pathstr
                    msg = 'unable to get subgroup %s'%(pathstr,)
                    raise ValueError, msg 
        return subgroup

    def _get_full_pathname(self,pathname):
        """
        Converts pathname to full pathname if it isn't already of that form.
        """
        pathlist = pathname.split('/')
        if len(pathlist) == 1:
            full_pathname = '/%s'%(pathname,)
        else:
            full_pathname = pathname
        return full_pathname


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import time
    logger = HDF5_Logger('sample.hdf5') 

    logger.add_group('/info')
    logger.add_datetime('/info')
    logger.add_attribute('/info', 'user', 'will dickson')
    logger.add_attribute('/info', 'notes', 'initial tests')
    logger.add_attribute('/info', 'mode', 'captive_trajectory')

    logger.add_dataset('/data/analog_input',(3,))
    logger.add_attribute('/data/analog_input', 'unit', 'V')

    logger.add_dataset('/data/distance/distance_raw', (1,))
    logger.add_attribute('/data/distance/distance_raw', 'unit', 'mm')

    logger.add_dataset('/data/distance/distance_kalman', (1,))
    logger.add_attribute('/data/distance/distance_kalman','unit', 'mm')

    logger.add_dataset('/data/distance/velocity_kalman', (1,))
    logger.add_attribute('/data/distance/velocity_kalman', 'unit', 'mm/s')

    logger.add_attribute('/data/distance', 'note', 'distance sensor data')

    for i in range(0,500):
        logger.add_dataset_value('/data/analog_input', [i, 2*i, 3*i])
        logger.add_dataset_value('/data/distance/distance_raw', i)
        logger.add_dataset_value('/data/distance/distance_kalman', i)
        logger.add_dataset_value('/data/distance/velocity_kalman', i)

    print len(logger.list('/'))

    del logger







