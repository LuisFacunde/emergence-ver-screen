import { useState } from 'react';
import { Search, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

const SearchPage = () => {
    const [query, setQuery] = useState('');

    const handleSearch = (e) => {
        e.preventDefault();
        console.log('Searching for:', query);
        // TODO: Implement actual search redirection or logic
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#0f172a] via-[#1e293b] to-[#0f172a] text-white flex flex-col items-center justify-center p-4">
            {/* Background decoration */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-500/10 rounded-full blur-[100px]" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/10 rounded-full blur-[100px]" />
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="w-full max-w-2xl relative z-10 flex flex-col items-center text-center"
            >
                <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                    Discover More
                </h1>
                <p className="text-gray-400 text-lg mb-10 max-w-lg">
                    Explore the vast universe of data with our advanced search engine.
                </p>

                <form onSubmit={handleSearch} className="w-full relative group">
                    <div className="relative flex items-center">
                        <Search className="absolute left-4 text-gray-400 w-5 h-5 group-focus-within:text-blue-400 transition-colors" />
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="What are you looking for?"
                            className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-12 text-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition-all shadow-lg backdrop-blur-sm"
                        />
                        <button
                            type="submit"
                            className="absolute right-2 p-2 bg-blue-600 hover:bg-blue-500 rounded-xl text-white transition-all hover:scale-105 active:scale-95"
                        >
                            <ArrowRight className="w-5 h-5" />
                        </button>
                    </div>
                </form>

                <div className="mt-8 flex gap-4 text-sm text-gray-500">
                    <span>Popular:</span>
                    <button className="hover:text-blue-400 transition-colors">Analytics</button>
                    <button className="hover:text-blue-400 transition-colors">Reports</button>
                    <button className="hover:text-blue-400 transition-colors">Users</button>
                </div>
            </motion.div>
        </div>
    );
};

export default SearchPage;
