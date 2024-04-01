import { styled } from "@mui/material";
import { useEffect, useState } from "react";
import { SERVER_URL } from "./Config";
import toast, { Toaster } from "react-hot-toast";

const Backdrop = styled("div")({
	position: "fixed",
	top: 0,
	left: 0,
	width: "100%",
	height: "100%",
	backgroundColor: "#010030",
	color: "white",
	zIndex: 100,
	display: "flex",
	flexDirection: "column",
	justifyContent: "center",
	alignItems: "center",
	fontFamily: 'Arial'
});

const SectionsContainer = styled("div")({
	display: "flex",
	flexDirection: "row",
	justifyContent: "space-around",
	width: "100%"
});

const Section = styled("div")({
	display: "flex",
	flexDirection: "column",
	border: "1px solid white",
	alignItems: "center",
	width: '35%',
	padding: '5px',
});

interface Data {
	clients: {
		add: string;
		current_level: number;
		current_subject: string;
		current_try: number;
		id: number;
		is_grading: boolean;
	}[],
	subjects: {
		[level: number]: {
			authorized_functions: string[];
			compiler_flags: string;
			function: string;
			main: string;
			name: string;
			send_trace: boolean;
			subject: string;
		}
	}
}

function App() {

	const [data, setData] = useState<null | Data>(null);

	const fetchData = async () => {
		const res = await fetch(SERVER_URL + '/status');
		if (!res.ok) {
			toast.error("Server is down");
			return;
		}
		setData(await res.json());
	}

	useEffect(() => {
		const interval = setInterval(() => {
			fetchData();
		}, 1000);
		return () => clearInterval(interval);
	}, [])

	return (
		<Backdrop>
			<Toaster position="top-center" reverseOrder={false} />
			<h1>Moulinette</h1>
			{
				data != null && (
					<SectionsContainer>
						<Section>
							<h2>Clients</h2>
						</Section>
						<Section>
							<h2>Subjects</h2>
						</Section>
					</SectionsContainer>
				)
			}
		</Backdrop>
	);
}

export default App;
