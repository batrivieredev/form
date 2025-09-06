import React from 'react';

const MessagesPage: React.FC = () => {
  return (
    <div>
      <div className="md:flex md:items-center md:justify-between mb-8">
        <div className="flex-1 min-w-0">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            Messages
          </h2>
        </div>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="divide-y divide-gray-200">
          {/* Will be replaced with actual messages */}
          <div className="p-4 sm:px-6">
            <div className="flex items-center justify-between">
              <div className="flex-1 min-w-0">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <span className="h-12 w-12 rounded-full bg-primary-100 flex items-center justify-center">
                      <svg
                        className="h-6 w-6 text-primary-600"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="2"
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                        />
                      </svg>
                    </span>
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-medium text-gray-900">
                      Example User
                    </h3>
                    <p className="text-sm text-gray-500">example@email.com</p>
                  </div>
                </div>
                <div className="mt-4">
                  <p className="text-sm text-gray-900">
                    This is an example message content. It will be replaced with actual messages from users.
                  </p>
                </div>
              </div>
              <div className="ml-6 flex-shrink-0">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  New
                </span>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              Received 2 hours ago
            </div>
          </div>
        </div>
      </div>

      {/* Empty state */}
      <div className="text-center mt-8 hidden">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No messages</h3>
        <p className="mt-1 text-sm text-gray-500">
          You have no messages at this time.
        </p>
      </div>
    </div>
  );
};

export default MessagesPage;
