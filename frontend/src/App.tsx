import { Navigate, Route, Routes } from "react-router-dom";
import { AmbientBackground } from "./components/AmbientBackground";
import { MainLayout } from "./components/MainLayout";
import { RequireAuth } from "./components/RequireAuth";
import { ThemeProvider } from "./context/ThemeContext";
import Landing from "./pages/Landing";
import Home from "./pages/Home";
import Track from "./pages/Track";
import MyPatterns from "./pages/Analytics";
import Chat from "./pages/Chat";
import Reminders from "./pages/Reminders";
import Settings from "./pages/Settings";
import Features from "./pages/Features";
import FAQs from "./pages/FAQs";
import AboutDiseases from "./pages/AboutDiseases";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import "./styles/animations.css";
import "./styles/hexagon.css";

export default function App() {
  return (
    <ThemeProvider>
      <AmbientBackground />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/features" element={<Features />} />
        <Route path="/faqs" element={<FAQs />} />
        <Route path="/about-diseases" element={<AboutDiseases />} />
        <Route element={<RequireAuth />}>
          <Route element={<MainLayout />}>
            <Route path="today" element={<Home />} />
            <Route path="track" element={<Track />} />
            <Route path="analytics" element={<MyPatterns />} />
            <Route path="chat" element={<Chat />} />
            <Route path="reminders" element={<Reminders />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </ThemeProvider>
  );
}
