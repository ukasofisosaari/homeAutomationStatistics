import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import { Link } from 'react-router-dom';

const styles = {
  root: {
    flexGrow: 1,
  },
};

const Navbar = () => (
  <nav>
    <AppBar position="static">
      <Toolbar>
        <Typography variant="title" color="inherit">
          Home Automation Statistics
        </Typography>
        <div style={{ marginLeft: '20px', display: 'inline-block' }}>
          <Typography
            variant="subheading"
            color="inherit"
            style={{ float: 'left', marginRight: '20px' }}
          >
            <Link style={{ color: 'unset', textDecoration: 'unset' }} to="/">
              Home
            </Link>
          </Typography>
          <Typography variant="subheading" color="inherit" style={{ float: 'left' }}>
            <Link style={{ color: 'unset', textDecoration: 'unset' }} to="/about">
              About
            </Link>
          </Typography>
        </div>
      </Toolbar>
    </AppBar>
  </nav>
);

export default withStyles(styles)(Navbar);
