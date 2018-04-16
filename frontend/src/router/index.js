import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import HomePage from '../components/HomePage';
import AboutPage from '../components/AboutPage';
import Navbar from '../components/utils/Navbar';

export default () => (
  <Router>
    <div>
      <Navbar />
      <Route exact path="/" component={HomePage} />
      <Route path="/about" component={AboutPage} />
    </div>
  </Router>
);
