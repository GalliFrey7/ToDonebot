from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# In-memory storage for tasks
tasks = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to the Task Manager Bot! Use the /menu command to see available commands.')

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task_description = ' '.join(context.args)
    if task_description:
        tasks.append({'description': task_description, 'done': False})
        await update.message.reply_text(f'Task added: {task_description}')
    else:
        await update.message.reply_text('Usage: /add <task description>')

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if tasks:
        task_list = '\n'.join([f"{i+1}. {'[x]' if task['done'] else '[ ]'} {task['description']}" for i, task in enumerate(tasks)])
        await update.message.reply_text(f'Your tasks:\n{task_list}')
    else:
        await update.message.reply_text('No tasks found.')

async def mark_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        task_index = int(context.args[0]) - 1
        if 0 <= task_index < len(tasks):
            tasks[task_index]['done'] = True
            await update.message.reply_text(f'Task {task_index + 1} marked as done.')
        else:
            await update.message.reply_text('Invalid task number.')
    except (IndexError, ValueError):
        await update.message.reply_text('Usage: /done <task number>')

async def clear_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global tasks
    tasks = []
    await update.message.reply_text('All tasks cleared.')

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menu_text = (
        "Menu commands:\n"
        "/start - Start working with the bot\n"
        "/add <task description> - Add a new task\n"
        "/list - Show task list\n"
        "/done <task number> - Mark a task as done\n"
        "/clear - Clear all tasks\n"
        "/menu - Show the menu commands"
    )
    await update.message.reply_text(menu_text)

def main() -> None:
    token = config('TELEGRAM_API_TOKEN')
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("list", list_tasks))
    application.add_handler(CommandHandler("done", mark_done))
    application.add_handler(CommandHandler("clear", clear_tasks))
    application.add_handler(CommandHandler("menu", show_menu))

    application.run_polling()

if __name__ == '__main__':
    main()
