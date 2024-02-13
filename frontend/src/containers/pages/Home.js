import React from 'react'; 
import { Link } from 'react-router-dom';

const home = () => (
    <div className='container'>
        <div className='mt-5 p-5 bg-light'>
            <h1 className='display-4'>Welcome to AO Investments</h1>
            <p className='lead'>
                This is a simple, beginner friendly portfolio tracker where you can track your crypto and stock investments all in one place 
                gaining valuable insights through graphs and key figures!  
            </p>
            <hr className='my-4' /> 
            <p>Click the button below to log in</p>
            <Link className='btn btn-primary btn-lg' to='/login'>Login</Link>
        </div>
    </div>
); 

export default home; 