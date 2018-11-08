import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
// import { Layout } from 'antd';
import HomePage from '../components/HomePage';
import AboutPage from '../components/AboutPage';
import Navbar from '../components/Navbar';
import Footer from '../components/layout/Footer';

export default () => (
  <Router>
    <div style={{ backgroundColor: '#EEEEEE', height: '100vh', width: '100%' }}>
      <Navbar />
      <Switch>
        <Route path="/about" component={AboutPage} />
        <Route path="/" component={HomePage} />
      </Switch>
      <Footer />
    </div>
  </Router>
);
