from zumi.zumi import Zumi
from zumi.util.screen import Screen
from zumi.protocol import Note
import os, subprocess, time, signal
from threading import Thread
from PIL import Image, ImageDraw
import numpy as np


def __progress(screen, img, start, end):
    while start != end:
        draw = ImageDraw.Draw(img)
        draw.point([(start + 13, 35), (start + 13, 36), (start + 13, 37)])
        screen.draw_image(img.convert('1'))
        start += 1


def __finished_updating(_internal_zumi, _screen, text):
    _zumi = _internal_zumi
    img = _screen.path_to_image('/usr/local/lib/python3.5/dist-packages/zumi/util/images/happy1.ppm')
    time.sleep(.5)
    _screen.draw_text(text, x=10, y=5, image=img.convert('1'), font_size=12, clear=False)

    tempo = 60
    time.sleep(0.5)
    _zumi.play_note(41, tempo)
    _zumi.play_note(43, tempo)
    _zumi.play_note(45, tempo)


def __kill_updater(proc, timeout):
    print("timeout!")
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    timeout["value"] = True


def update_version(_zumi, _screen, v=None):
    if v is None:
        _screen.draw_text_center("didn't get the version number try again")
        return False
    p = subprocess.Popen('sudo pip3 install zumidashboard=={}'.format(v),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    img_arr = np.asarray(Image.open('/usr/local/lib/python3.5/dist-packages/zumi/util/images/blankbar.ppm'))
    img = Image.fromarray(img_arr.astype('uint8'))

    _screen.draw_text("I'm updating", x=9, y=8, image=img.convert('1'), font_size=12, clear=False)
    img = _screen.screen_image.convert('RGB')

    updater_thread = Thread(target=__progress, args=(_screen,img, 0, 51))
    updater_thread.start()

    try:
        while p.poll() is None:
            line = p.stdout.readline().decode()
            print(line)

            if 'Error' in line:
                updater_thread.join()
                _screen.draw_text_center("Couldn't update, please try again")
                time.sleep(1)
                _zumi.play_note(Note.A5, 100)
                _zumi.play_note(Note.F5, 2 * 100)
                time.sleep(7)
                return False

            if 'Collecting' in line:
                updater_thread.join()
                updater_thread = Thread(target=__progress, args=(_screen, img, 51, 88))
                updater_thread.start()

            elif 'Installing collected packages' in line:
                updater_thread.join()
                updater_thread = Thread(target=__progress, args=(_screen, img, 88, 96))
                updater_thread.start()

            elif 'Successfully installed' in line:
                updater_thread.join()
                updater_thread = Thread(target=__progress, args=(_screen, img, 96, 101))
                updater_thread.start()
                version_info = line.split('-')[-1]

        print(version_info)
        updater_thread.join()

        time.sleep(1)
        __finished_updating(_zumi, _screen, "I'm updated!")
        time.sleep(2)
        _screen.draw_text_center("Zumi updated to v" + str(version_info), font_size=15)

    except Exception as e:
        updater_thread.join()
        _screen.draw_text_center("Zumi already up-to-date")
        print(e)
    return True


def update_content(_zumi, _screen, _language='en'):
    path = '/home/pi/Dashboard/'
    if _language == 'ko':
        git_url = 'git clone https://github.com/robolink-korea/zumi_kor_lesson.git '
    else:
        git_url = 'git clone https://github.com/RobolinkInc/Zumi_Content.git '

    log_folder = _change_to_log_folder(_language)
    img = Image.fromarray(
        np.asarray(Image.open('/usr/local/lib/python3.5/dist-packages/zumi/util/images/blankbar.ppm')).astype('uint8'))
    _screen.draw_text("Updating Content", x=12, y=8, image=img.convert('1'), font_size=12, clear=False)
    img = _screen.screen_image.convert('RGB')

    p = subprocess.Popen(
        git_url + path + 'Zumi_Content_'+_language,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
    print("start clone")

    time.sleep(1)
    try:
        content_updater_thread = Thread(target=__progress, args=(_screen, img, 0, 101))
        while p.poll() is None:
            line = p.stdout.readline().decode()
            print(line)

            if 'Cloning into ' in line:
                content_updater_thread.start()

            elif 'fatal: ' in line:
                content_updater_thread.join()
                _roll_back_folder(_screen, _zumi, log_folder, path)
                return False

            elif 'Already up-to-date' in line:
                _screen.draw_text_center('Zumi content is already latest')
                break
        if content_updater_thread.is_alive():
            content_updater_thread.join()
    except:
        if content_updater_thread.is_alive():
            content_updater_thread.join()
        print("Couldn't update, please try again")
        _roll_back_folder(_screen, _zumi, log_folder, path)
        return False
    time.sleep(2)
    subprocess.Popen("sudo chown -R pi " + path + "Zumi_Content_"+_language,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    # update_lessonlist_file()
    updated_version = open(path + 'Zumi_Content_{}/README.md'.format(_language)).readline().split()[0]
    __finished_updating(_zumi, _screen, "Updated to v{} !".format(updated_version))

    time.sleep(3)
    return True


def _roll_back_folder(_screen, _zumi, log_folder, path, language):
    if log_folder is not None:
        print("revert folder")
        subprocess.Popen("sudo rm -rf /home/pi/Dashboard/Zumi_Content_"+language,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        time.sleep(1)
        subprocess.Popen('mv ' + log_folder + " " + path + "Zumi_Content_"+language,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        time.sleep(2)
        subprocess.Popen("sudo chown -R pi " + path + "Zumi_Content_"+language,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    _screen.draw_text_center("Couldn't update, please try again")
    time.sleep(1)
    _zumi.play_note(Note.A5, 100)
    _zumi.play_note(Note.F5, 2 * 100)
    time.sleep(7)


def _change_to_log_folder(language, path='/home/pi/Dashboard/'):
    if not os.path.isdir("{}content_history".format(path)):
        os.mkdir("{}content_history".format(path))

    current = None
    try:
        current = open(path+'Zumi_Content_{}/README.md'.format(language)).readline().split()[0]
    except FileNotFoundError:
        print("content folder is not exist")
        return current

    folder_name = 'content_history/log_v{}_content_{}'.format(str(current), language)
    log_folder = path + folder_name
    cnt = 1
    while os.path.isdir(log_folder):
        log_folder = path + folder_name + '_{}'.format(cnt)
        cnt += 1
    subprocess.Popen('mv ' + path + 'Zumi_Content_{} '.format(language) + log_folder,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    time.sleep(2)
    subprocess.Popen("sudo chown -R pi " + log_folder,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    print("change name : {}".format(log_folder))
    return log_folder


def restart_threads(_screen):
    Thread(target=restart_app, args=()).start()
    Thread(target=go_to_zumi_dashboard_msg, args=(_screen,)).start()


def restart_app():
    subprocess.run(["sudo systemctl restart zumidashboard.service"], shell=True)


def go_to_zumi_dashboard_msg(_screen):
    lib_dir = os.path.dirname(os.path.abspath(__file__))
    _screen.draw_text_center("Dashboard restarting...")
    while True:
        p = subprocess.Popen(
            ['sudo', 'bash', lib_dir + '/shell_scripts/check_port.sh', '80'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        p.wait()
        if len(stdout) > 1:
            print("server(port 80) is not ready")
        else:
            print("server(port 80) is ready")
            break
        time.sleep(2)
    _screen.draw_text_center("Go to \"zumidashboard.ai\" in your browser")


def check_user_content(base_dir_path, usr_dir_path, language):
    try:
        base = open(base_dir_path + 'Zumi_Content_{}/README.md'.format(language)).readline().split()[0]
    except:
        return True
    try:
        usr_version = open(usr_dir_path+'Zumi_Content_{}/README.md'.format(language)).readline().split()[0]
    except:
        return True

    if usr_version != base:
        return True
    else:
        return False


def copy_content(base_dir_path, usr_dir_path, language):
    _change_to_log_folder(language, usr_dir_path)
    p = subprocess.Popen(['cp', '-r', base_dir_path + 'Zumi_Content_' + language, usr_dir_path])
    stdout, stderr = p.communicate()
    print("done copy")
    time.sleep(2)
    p = subprocess.Popen("sudo chown -R pi:pi " + usr_dir_path + 'Zumi_Content_'+language,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = p.communicate()
    print("done change permition")

def update_develop_version(_zumi, _screen):
    option = '--upgrade'
    git_url = 'https://develop:ehhwu3qQn5Es5aJVuFS9@gitlab.com/robolink-team/Flask-AP.git@develop#egg=zumidashboard'
    p = subprocess.Popen('sudo pip3 install {} git+{}'.format(option, git_url),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    img_arr = np.asarray(Image.open('/usr/local/lib/python3.5/dist-packages/zumi/util/images/blankbar.ppm'))
    img = Image.fromarray(img_arr.astype('uint8'))

    _screen.draw_text("Updating from git", x=9, y=8, image=img.convert('1'), font_size=12, clear=False)
    img = _screen.screen_image.convert('RGB')

    updater_thread = Thread(target=__progress, args=(_screen,img, 0, 21))
    updater_thread.start()

    try:
        while p.poll() is None:
            line = p.stdout.readline().decode()
            print(line)

            if 'Error' in line:
                updater_thread.join()
                _screen.draw_text_center("Couldn't update, please try again")
                time.sleep(1)
                _zumi.play_note(Note.A5, 100)
                _zumi.play_note(Note.F5, 2 * 100)
                time.sleep(7)
                return False

            if 'Cloning' in line:
                updater_thread.join()
                updater_thread = Thread(target=__progress, args=(_screen, img, 21, 88))
                updater_thread.start()

            elif 'Installing collected packages' in line:
                updater_thread.join()
                updater_thread = Thread(target=__progress, args=(_screen, img, 88, 96))
                updater_thread.start()

            elif 'Successfully installed' in line:
                updater_thread.join()
                updater_thread = Thread(target=__progress, args=(_screen, img, 96, 101))
                updater_thread.start()
                version_info = line.split('-')[-1]

        print(version_info)
        updater_thread.join()

        time.sleep(1)
        __finished_updating(_zumi, _screen, "Dashboard updated!")
        _screen.draw_text_center("Dashboard updated to v" + str(version_info), font_size=15)

    except Exception as e:
        updater_thread.join()
        _screen.draw_text_center("Couldn't update, please try again")
        time.sleep(1)
        _zumi.play_note(Note.A5, 100)
        _zumi.play_note(Note.F5, 2 * 100)
        time.sleep(7)
        return False
    return True


def update_eveything_pipeline(_zumi, _screen, v, language='en'):
    update_success = update_version(_zumi, _screen, v)
    time.sleep(2)
    if update_success:
        update_content(_zumi, _screen, language)
    restart_threads(_screen)


def update_dashboard_pipeline(_zumi, _screen, v):
    update_version(_zumi, _screen, v)
    time.sleep(2)
    restart_threads(_screen)


def update_develop_pipeline(_zumi, _screen):
    update_develop_version(_zumi, _screen)
    time.sleep(2)
    restart_threads(_screen)


def run_develop():
    zumi = Zumi()
    screen = Screen(clear=False)
    update_develop_pipeline(zumi, screen)


def run(v=None):
    zumi = Zumi()
    screen = Screen(clear=False)
    update_dashboard_pipeline(zumi, screen, v)


def run_everything(v=None, language='en'):
    zumi = Zumi()
    screen = Screen(clear=False)
    update_eveything_pipeline(zumi, screen, v, language)


if __name__ == '__main__':
    import sys
    lib_dir = os.path.dirname(os.path.abspath(__file__))
    p = subprocess.Popen(
        ['sudo', 'bash', lib_dir+'/shell_scripts/check_port.sh', '80'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    p.wait()
    if len(stdout) > 1:
        print("server(port 80) is not ready")
    else:
        print("server(port 80) is ready")
        p = subprocess.Popen(['sudo', 'systemctl', 'stop', 'zumidashboard.service'])

    if sys.argv[1] == "develop":
        run_develop()
    elif sys.argv[2] == "None":
        run(sys.argv[1])
    else:
        run_everything(sys.argv[1], sys.argv[2])
