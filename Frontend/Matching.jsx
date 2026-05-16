import { motion } from "framer-motion";

export default function Matching() {
  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-[#1e3c72] via-[#2a5298] to-[#4facfe]">

      {/* Card */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="bg-white/90 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-[340px] text-center"
      >

        {/* Avatar */}
        <div className="text-5xl mb-3">👩</div>

        {/* User Info */}
        <h2 className="text-2xl font-bold text-gray-800 mb-1">
          Riya 👋
        </h2>

        <p className="text-gray-600">
          🌍 Native: <span className="font-medium">Bengali</span>
        </p>

        <p className="text-gray-600">
          🎯 Learning: <span className="font-medium">Hindi</span>
        </p>

        <p className="text-gray-500 mt-2 text-sm">
          ❤️ Interests: Travel, Food, Music
        </p>

        {/* Buttons */}
        <div className="flex justify-between mt-6 gap-4">

          {/* Skip */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.9 }}
            className="w-1/2 bg-red-400 hover:bg-red-500 text-white py-2 rounded-lg shadow-md"
          >
            Skip ❌
          </motion.button>

          {/* Connect */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.9 }}
            className="w-1/2 bg-green-500 hover:bg-green-600 text-white py-2 rounded-lg shadow-md"
          >
            Connect ❤️
          </motion.button>

        </div>

      </motion.div>
    </div>
  );
}