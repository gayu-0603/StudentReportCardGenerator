import React, { useState, useMemo } from 'react';
import { User, BookOpen, Award, Calculator, PlusCircle, Trash2, GraduationCap } from 'lucide-react';

const SUBJECTS = ["Math", "Science", "English", "History", "Geography"];

const App = () => {
  const [students, setStudents] = useState([]);
  const [currentStudent, setCurrentStudent] = useState({
    id: '',
    name: '',
    marks: {
      Math: '',
      Science: '',
      English: '',
      History: '',
      Geography: ''
    }
  });

  const calculateGrade = (average) => {
    if (average >= 90) return { label: "A+", color: "text-green-600 bg-green-50" };
    if (average >= 80) return { label: "A", color: "text-blue-600 bg-blue-50" };
    if (average >= 70) return { label: "B", color: "text-indigo-600 bg-indigo-50" };
    if (average >= 60) return { label: "C", color: "text-yellow-600 bg-yellow-50" };
    if (average >= 50) return { label: "D", color: "text-orange-600 bg-orange-50" };
    return { label: "F", color: "text-red-600 bg-red-50" };
  };

  const handleMarkChange = (subject, value) => {
    // Ensure input is between 0 and 100
    const numValue = value === '' ? '' : Math.min(100, Math.max(0, parseFloat(value) || 0));
    setCurrentStudent(prev => ({
      ...prev,
      marks: { ...prev.marks, [subject]: numValue }
    }));
  };

  const addStudent = (e) => {
    e.preventDefault();
    if (!currentStudent.id || !currentStudent.name) return;

    const scores = Object.values(currentStudent.marks).map(m => parseFloat(m) || 0);
    const total = scores.reduce((sum, s) => sum + s, 0);
    const average = total / SUBJECTS.length;
    const gradeInfo = calculateGrade(average);

    const newEntry = {
      ...currentStudent,
      total,
      average,
      grade: gradeInfo.label,
      gradeColor: gradeInfo.color,
      timestamp: new Date().toLocaleTimeString()
    };

    setStudents([newEntry, ...students]);
    
    // Reset form
    setCurrentStudent({
      id: '',
      name: '',
      marks: Object.fromEntries(SUBJECTS.map(s => [s, '']))
    });
  };

  const removeStudent = (index) => {
    setStudents(students.filter((_, i) => i !== index));
  };

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8 font-sans text-slate-900">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <header className="mb-8 flex items-center gap-3">
          <div className="bg-indigo-600 p-3 rounded-xl text-white">
            <GraduationCap size={32} />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-slate-800">Student Report System</h1>
            <p className="text-slate-500">Generate and manage academic performance records</p>
          </div>
        </header>

        <div className="grid lg:grid-cols-12 gap-8">
          
          {/* Input Form */}
          <div className="lg:col-span-4">
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sticky top-8">
              <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <PlusCircle size={20} className="text-indigo-600" />
                New Entry
              </h2>
              
              <form onSubmit={addStudent} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Student ID</label>
                  <input 
                    required
                    type="text"
                    className="w-full px-4 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                    placeholder="e.g. STU-101"
                    value={currentStudent.id}
                    onChange={(e) => setCurrentStudent({...currentStudent, id: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
                  <input 
                    required
                    type="text"
                    className="w-full px-4 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                    placeholder="e.g. Jane Doe"
                    value={currentStudent.name}
                    onChange={(e) => setCurrentStudent({...currentStudent, name: e.target.value})}
                  />
                </div>

                <div className="pt-4 border-t border-slate-100">
                  <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-3">Subject Marks (0-100)</h3>
                  <div className="space-y-3">
                    {SUBJECTS.map(subject => (
                      <div key={subject} className="flex items-center justify-between gap-4">
                        <label className="text-sm text-slate-600">{subject}</label>
                        <input 
                          required
                          type="number"
                          className="w-20 px-3 py-1.5 rounded-lg border border-slate-200 text-right outline-none focus:border-indigo-500"
                          value={currentStudent.marks[subject]}
                          onChange={(e) => handleMarkChange(subject, e.target.value)}
                        />
                      </div>
                    ))}
                  </div>
                </div>

                <button 
                  type="submit"
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl transition-colors shadow-lg shadow-indigo-100 mt-4"
                >
                  Generate Report
                </button>
              </form>
            </div>
          </div>

          {/* Report List */}
          <div className="lg:col-span-8 space-y-6">
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-xl font-semibold text-slate-800 flex items-center gap-2">
                <BookOpen size={20} className="text-indigo-600" />
                Active Reports ({students.length})
              </h2>
            </div>

            {students.length === 0 ? (
              <div className="bg-white border-2 border-dashed border-slate-200 rounded-2xl p-12 text-center">
                <div className="bg-slate-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Calculator className="text-slate-300" size={32} />
                </div>
                <h3 className="text-slate-500 font-medium">No reports generated yet</h3>
                <p className="text-slate-400 text-sm">Enter student details on the left to begin.</p>
              </div>
            ) : (
              <div className="grid sm:grid-cols-2 gap-6">
                {students.map((student, idx) => (
                  <div key={idx} className="bg-white rounded-2xl shadow-md border border-slate-100 overflow-hidden group">
                    <div className="p-5 border-b border-slate-50 bg-slate-50/50 flex justify-between items-start">
                      <div>
                        <div className="text-xs font-bold text-indigo-500 mb-1">{student.id}</div>
                        <h3 className="text-lg font-bold text-slate-800">{student.name}</h3>
                      </div>
                      <button 
                        onClick={() => removeStudent(idx)}
                        className="text-slate-300 hover:text-red-500 transition-colors p-1"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                    
                    <div className="p-5">
                      <div className="space-y-2 mb-6">
                        {Object.entries(student.marks).map(([sub, score]) => (
                          <div key={sub} className="flex justify-between text-sm">
                            <span className="text-slate-500">{sub}</span>
                            <span className="font-semibold text-slate-700">{score.toFixed(1)}</span>
                          </div>
                        ))}
                      </div>

                      <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                        <div>
                          <p className="text-xs text-slate-400 uppercase font-bold tracking-tighter">Average Score</p>
                          <p className="text-2xl font-black text-slate-800">{student.average.toFixed(2)}%</p>
                        </div>
                        <div className={`px-4 py-2 rounded-xl text-center font-bold text-xl ${student.gradeColor}`}>
                          {student.grade}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
