import React, { useEffect, useState } from "react"
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { login } from "../services/ApiServices.js";

export const Home = () => {

	const [userData, setUserData] = useState({
		email: "",
		password: ""
	})

	const handleSubmit = (e) => {
		e.preventDefault()
		if (!userData.email || !userData.password) {
			alert("All fields are required");
			return;
		}
		login(userData)

	}

	const handleChange = (e) => {
		setUserData({
			...userData,
			[e.target.name]: e.target.value
		})
	}

	return (
		<div className="container mt-5">
			<form onSubmit={handleSubmit}>
				<div className="mb-3">
					<label htmlFor="email" className="form-label">Email address</label>
					<input type="email" className="form-control" id="email" name="email" onChange={handleChange} />
				</div>
				<div className="mb-3">
					<label htmlFor="password" className="form-label">Password</label>
					<input type="password" className="form-control" id="password" name="password" onChange={handleChange} />
				</div>

				<button type="submit" className="btn btn-primary">Submit</button>
			</form>
		</div>
	);
}; 