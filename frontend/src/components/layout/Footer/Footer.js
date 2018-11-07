import React from 'react';
import Typography from '@material-ui/core/Typography';

export default () => (
  <div
    style={{
      position: 'fixed',
      left: 0,
      bottom: 0,
      width: '100%',
      backgroundColor: '#F5F5F5',
      color: 'black',
      textAlign: 'center',
    }}
  >
    <footer>
      <Typography variant="subheading">Footer!</Typography>
    </footer>
  </div>
);
