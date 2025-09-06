import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface NavItemProps {
  to: string;
  children: React.ReactNode;
  currentPath: string;
}

const NavItem: React.FC<NavItemProps> = ({ to, children, currentPath }) => {
  const isActive = currentPath === to;
  return (
    <Link
      to={to}
      className={`px-4 py-2 rounded-lg transition-colors duration-150 ${
        isActive
          ? 'bg-primary-100 text-primary-800'
          : 'text-gray-600 hover:bg-gray-100'
      }`}
    >
      {children}
    </Link>
  );
};

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { logout, user } = useAuth();
  const location = useLocation();

  const getInitials = (email: string) => {
    return email.split('@')[0].charAt(0).toUpperCase();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex space-x-4">
              <NavItem to="/" currentPath={location.pathname}>
                Dashboard
              </NavItem>
              <NavItem to="/forms" currentPath={location.pathname}>
                Forms
              </NavItem>
              <NavItem to="/messages" currentPath={location.pathname}>
                Messages
              </NavItem>
              {(user?.role === 'super_admin' || user?.role === 'sub_admin') && (
                <NavItem to="/tickets" currentPath={location.pathname}>
                  Tickets
                </NavItem>
              )}
              {user?.role === 'super_admin' && (
                <NavItem to="/admin" currentPath={location.pathname}>
                  Admin
                </NavItem>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center">
                <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                  <span className="text-sm font-medium text-primary-700">
                    {user?.email ? getInitials(user.email) : '?'}
                  </span>
                </div>
                <span className="ml-3 text-sm font-medium text-gray-700">
                  {user?.email}
                </span>
              </div>
              <button
                onClick={logout}
                className="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">{children}</div>
      </main>
    </div>
  );
};

export default Layout;
