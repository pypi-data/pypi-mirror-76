import py_cui

from pymusicterm.ui.progressbar import LoadingBarWidget

class CustomWidgetSet(py_cui.widget_set.WidgetSet):
    def __init__(self,num_rows,num_cols,logger,simulated_terminal) -> None:
        """ Initializer for WidgetSet
        """
        super().__init__(num_rows,num_cols,logger,simulated_terminal)

    def add_progress_bar(self, row, column, row_span = 1, column_span = 1, padx = 1, pady = 0,title="00:00"):
        """ Functions that adds a new progress bar to the CUI grid

        Parameters
        ----------
        row : int
            Row value from the top down
        column : int 
            Column from the top down
        row_span=1 :int
            Number of rows to span across
        column_span=1 : int
            Number of columns to span across
        padx=1 : int
            Number of padding characters in the x direction
        pady=0 : int
            Number of padding characters in the y direction
        title='00:00' : str
            Title of the duration of the song
        """
        id='Widget{}'.format(len(self._widgets.keys()))
        new_progress_bar=LoadingBarWidget(id,title,self._grid,row,column,row_span,
        column_span,padx,pady,self._logger)

        self._widgets[id]=new_progress_bar
        self._logger.debug('Adding widget {} w/ ID {} of type {}'.format(title,id,str(type(new_progress_bar))))

        return new_progress_bar
