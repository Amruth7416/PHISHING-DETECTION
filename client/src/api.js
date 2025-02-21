import axios from "axios";

export const detectAttack = async (text) => {
  try {
    const response = await axios.post("http://127.0.0.1:5000/detect", { text });
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    return { risk: "unknown", message: "Error detecting attack" };
  }
};
