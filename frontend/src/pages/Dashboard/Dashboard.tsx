import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Link } from 'react-router-dom';
import {
  DocumentTextIcon,
  UserGroupIcon,
  EnvelopeIcon,
  ClipboardDocumentListIcon,
} from '@heroicons/react/24/outline';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();

  const getDisplayName = (user: { username?: string; email: string }) => {
    return user.username || user.email.split('@')[0];
  };

  const SuperAdminDashboard = () => (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <Link
        to="/sites"
        className="col-span-1 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
      >
        <div className="p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
              <UserGroupIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Sites Management</h3>
              <p className="mt-1 text-sm text-gray-500">
                Manage all sites and their administrators
              </p>
            </div>
          </div>
        </div>
      </Link>

      <Link
        to="/messages"
        className="col-span-1 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
      >
        <div className="p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
              <EnvelopeIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Messages</h3>
              <p className="mt-1 text-sm text-gray-500">
                View and respond to site admin inquiries
              </p>
            </div>
          </div>
        </div>
      </Link>
    </div>
  );

  const SiteAdminDashboard = () => (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <Link
        to="/forms"
        className="col-span-1 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
      >
        <div className="p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
              <DocumentTextIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Forms</h3>
              <p className="mt-1 text-sm text-gray-500">
                Create and manage forms for your site
              </p>
            </div>
          </div>
        </div>
      </Link>

      <Link
        to="/messages"
        className="col-span-1 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
      >
        <div className="p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
              <EnvelopeIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Messages</h3>
              <p className="mt-1 text-sm text-gray-500">
                Communicate with users and view submissions
              </p>
            </div>
          </div>
        </div>
      </Link>
    </div>
  );

  const UserDashboard = () => (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <Link
        to="/forms"
        className="col-span-1 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
      >
        <div className="p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
              <ClipboardDocumentListIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">My Forms</h3>
              <p className="mt-1 text-sm text-gray-500">
                View and fill out available forms
              </p>
            </div>
          </div>
        </div>
      </Link>

      <Link
        to="/messages"
        className="col-span-1 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
      >
        <div className="p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
              <EnvelopeIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Messages</h3>
              <p className="mt-1 text-sm text-gray-500">
                View messages and communicate with administrators
              </p>
            </div>
          </div>
        </div>
      </Link>
    </div>
  );

  return (
    <div className="py-6">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">
          Welcome, {user && getDisplayName(user)}!
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          {user?.role === 'super_admin'
            ? 'Manage your form system and sites'
            : user?.role === 'site_admin'
            ? 'Manage your site forms and users'
            : 'View and submit your forms'}
        </p>
      </div>

      {user?.role === 'super_admin' ? (
        <SuperAdminDashboard />
      ) : user?.role === 'site_admin' ? (
        <SiteAdminDashboard />
      ) : (
        <UserDashboard />
      )}
    </div>
  );
};

export default Dashboard;
