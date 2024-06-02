import maya.cmds as cmds
import os
import time
import threading

def set_project_on_scene_open():
    # 現在のシーンのファイルパスを取得
    scene_path = cmds.file(query=True, sceneName=True)
    
    if scene_path:
        # シーンファイルのディレクトリを取得
        scene_dir = os.path.dirname(scene_path)
        
        # workspace.melのあるディレクトリを見つける
        workspace_mel_dir = find_workspace_mel_dir(scene_dir)
        
        if workspace_mel_dir:
            # workspace.melが見つかったディレクトリをプロジェクトとして設定
            cmds.workspace(workspace_mel_dir, openWorkspace=True)
            print(f"Project set to: {workspace_mel_dir}")
            start_autosave(workspace_mel_dir, scene_path)
        else:
            print("Workspace.mel not found in parent directories. Project not set.")
    else:
        print("No scene open. Project not set.")

def find_workspace_mel_dir(start_dir):
    # start_dirから上位ディレクトリを再帰的に検索してworkspace.melを見つける
    current_dir = start_dir
    while current_dir:
        workspace_mel_path = os.path.join(current_dir, "workspace.mel")
        if os.path.exists(workspace_mel_path):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            # ルートディレクトリに到達した場合、探索を終了
            break
        current_dir = parent_dir
    return None

def start_autosave(project_dir, scene_path):
    # オートセーブディレクトリを作成
    scene_name = os.path.splitext(os.path.basename(scene_path))[0]
    autosave_dir = os.path.join(project_dir, 'autosave', scene_name)
    if not os.path.exists(autosave_dir):
        os.makedirs(autosave_dir)
    
    # オートセーブスレッドを開始
    autosave_thread = threading.Thread(target=autosave_function, args=(autosave_dir, scene_name))
    autosave_thread.daemon = True  # スレッドがメインスレッドと共に終了するように設定
    autosave_thread.start()

def autosave_function(autosave_dir, scene_name):
    while True:
        # 10分ごとにシーンを保存
        time.sleep(600)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(autosave_dir, f"{scene_name}_{timestamp}.ma")
        cmds.file(rename=save_path)
        cmds.file(save=True, type='mayaAscii')
        print(f"Auto-saved scene to: {save_path}")

# コールバックを登録
callbacks = []

def register_callbacks():
    global callbacks
    callbacks.append(cmds.scriptJob(event=["SceneOpened", set_project_on_scene_open], protected=True))

def unregister_callbacks():
    global callbacks
    for callback in callbacks:
        cmds.scriptJob(kill=callback, force=True)
    callbacks = []

# Mayaの起動時にコールバックを登録
register_callbacks()
