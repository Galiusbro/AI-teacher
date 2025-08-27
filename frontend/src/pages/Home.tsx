import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🎓 Ayaal Teacher
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Интеллектуальная платформа персонализированного обучения с системой Mastery
          </p>
        </header>

        {/* Navigation Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {/* Registration Card */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="text-3xl mb-4">👨‍👩‍👧‍👦</div>
            <h3 className="text-xl font-semibold mb-3">Регистрация</h3>
            <p className="text-gray-600 mb-4">
              Создайте аккаунт для себя или вашего ребенка
            </p>
            <div className="space-y-2">
              <Link
                to="/register/parent"
                className="block w-full bg-blue-600 text-white text-center py-2 px-4 rounded hover:bg-blue-700 transition-colors"
              >
                Регистрация родителя
              </Link>
              <Link
                to="/register/student"
                className="block w-full bg-green-600 text-white text-center py-2 px-4 rounded hover:bg-green-700 transition-colors"
              >
                Регистрация ученика
              </Link>
            </div>
          </div>

          {/* Login Card */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="text-3xl mb-4">🔐</div>
            <h3 className="text-xl font-semibold mb-3">Вход в систему</h3>
            <p className="text-gray-600 mb-4">
              Войдите в свой аккаунт для доступа к обучению
            </p>
            <Link
              to="/login"
              className="block w-full bg-indigo-600 text-white text-center py-2 px-4 rounded hover:bg-indigo-700 transition-colors"
            >
              Войти
            </Link>
          </div>

          {/* Demo Card */}
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="text-3xl mb-4">🚀</div>
            <h3 className="text-xl font-semibold mb-3">Демо режим</h3>
            <p className="text-gray-600 mb-4">
              Попробуйте систему без регистрации
            </p>
            <Link
              to="/demo"
              className="block w-full bg-purple-600 text-white text-center py-2 px-4 rounded hover:bg-purple-700 transition-colors"
            >
              Запустить демо
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-center mb-8">✨ Возможности платформы</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="flex items-start space-x-3">
              <div className="text-2xl">🧠</div>
              <div>
                <h4 className="font-semibold">Система Mastery</h4>
                <p className="text-gray-600">Умная оценка уровня освоения материала</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="text-2xl">📚</div>
              <div>
                <h4 className="font-semibold">Персонализированные уроки</h4>
                <p className="text-gray-600">Адаптивное обучение под каждого ученика</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="text-2xl">🎯</div>
              <div>
                <h4 className="font-semibold">AI генерация контента</h4>
                <p className="text-gray-600">Создание уникальных заданий с помощью ИИ</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="text-2xl">📊</div>
              <div>
                <h4 className="font-semibold">Детальная аналитика</h4>
                <p className="text-gray-600">Отслеживание прогресса и результатов</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
