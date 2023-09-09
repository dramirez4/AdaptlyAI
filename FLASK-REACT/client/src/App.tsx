// Import necessary React hooks and components
import { useState, useEffect } from 'react';

// Define the main App component
function App() {
  // Initialize a state variable called 'data' using the 'useState' hook,
  // with an initial value of an array containing an empty object.
  const [data, setData] = useState([{}]);

  // Use the 'useEffect' hook to perform side effects in the component.
  // In this case, it fetches data from the '/members' endpoint when the
  // component mounts (empty dependency array).
  useEffect(() => {
    fetch(import.meta.env.VITE_PUBLIC_API_URL + "/members") // Send a GET request to the '/members' endpoint
      .then((res) => res.json()) // Parse the response as JSON
      .then((data) => {
        // Update the 'data' state variable with the fetched data
        setData(data);
        console.log(data); // Log the fetched data to the console
      });
  }, []); // The empty dependency array ensures this effect runs only once.

  // Render the component's UI
  return (
    <div>
      {/* Conditional rendering based on the presence of 'data.members' */}
      {typeof data.members === 'undefined' ? (
        <p>loading..</p> // Display a loading message when data is being fetched
      ) : (
        // Map over the 'data.members' array and display each member as a paragraph
        data.members.map((member, i) => (
          <p key={i}>{member}</p>
        ))
      )}
    </div>
  );
}

// Export the App component as the default export of this module
export default App;

