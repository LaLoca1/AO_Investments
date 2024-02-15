import React, { Fragment } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { connect } from 'react-redux';
import { logout } from '../../actions/auth';
import './Sidebar.css';

const Sidebar = ({ isAuthenticated, logout }) => {
    const authLinks = (
        <Fragment>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/dashboard'>Stocks Dashboard</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/stockportfolio'>Stocks Portfolio</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/cryptodashboard'>Crypto Dashboard</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/cryptoportfolio'>Crypto Portfolio</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/combinedportfolio'>Overall Portfolio</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/news'>News Section</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/userprofile'>User Profile</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/' onClick={logout}>Logout</NavLink>
            </li>
        </Fragment>
    );

    const guestLinks = (
        <Fragment>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/'>Home</NavLink>
            </li>
        </Fragment>
    );

    return (
        <nav className='sidebar'>
            <div className='sidebar-header'>
                <Link className='navbar-brand'>AO Investments</Link>
            </div>
            <ul className='nav flex-column'>
                { isAuthenticated ? authLinks : guestLinks }
            </ul>
        </nav>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { logout })(Sidebar);
