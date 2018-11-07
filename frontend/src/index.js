import React from 'react';
import { render } from 'react-dom';
import CssBaseline from '@material-ui/core/CssBaseline';
import Router from './router';

render(
  <React.Fragment>
    <CssBaseline>
      <Router />
    </CssBaseline>
  </React.Fragment>,
  document.getElementById('app'),
);
