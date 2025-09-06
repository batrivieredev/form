import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import FormListPage from './pages/FormListPage';
import FormDetailPage from './pages/FormDetailPage';
import MessagesPage from './pages/MessagesPage';
import AdminPage from './pages/AdminPage';
import TicketManagementPage from './pages/TicketManagementPage';
import Layout from './components/Layout';
import { AuthProvider } from './contexts/AuthContext';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="font-sans min-h-screen bg-gray-50">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <Layout>
                    <DashboardPage />
                  </Layout>
                </PrivateRoute>
              }
            />
            <Route
              path="/forms"
              element={
                <PrivateRoute>
                  <Layout>
                    <FormListPage />
                  </Layout>
                </PrivateRoute>
              }
            />
            <Route
              path="/forms/:id"
              element={
                <PrivateRoute>
                  <Layout>
                    <FormDetailPage />
                  </Layout>
                </PrivateRoute>
              }
            />
            <Route
              path="/messages"
              element={
                <PrivateRoute>
                  <Layout>
                    <MessagesPage />
                  </Layout>
                </PrivateRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <PrivateRoute>
                  <Layout>
                    <AdminPage />
                  </Layout>
                </PrivateRoute>
              }
            />
            <Route
              path="/tickets"
              element={
                <PrivateRoute>
                  <Layout>
                    <TicketManagementPage />
                  </Layout>
                </PrivateRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
