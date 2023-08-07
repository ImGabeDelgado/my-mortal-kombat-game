import pygame

class Fighter():

    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self._player = player
        self._size = data[0]
        self._image_scale = data[1]
        self._offset = data[2]
        self._flip = flip
        self._animation_list = self.load_images(sprite_sheet, animation_steps)
        self._action = 4 # 0:attack1 1:attack2 2:death 3:fall 4:idle 5:jump 6:run 7:take hit
        self._frame_index = 0
        self._image = self._animation_list[self._action][self._frame_index]
        self._update_time = pygame.time.get_ticks()
        self._rect = pygame.Rect((x, y, 80, 180))
        self._vel_y = 0
        self._running = False
        self._jump = False
        self._attacking = False
        self._attack_type = 0
        self._attack_cooldown = 0
        self._hit = False
        self._health = 100
        self._alive = True

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for i in range(animation):
                temp_img = sprite_sheet.subsurface(i * self._size, y * self._size, self._size, self._size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self._size * self._image_scale, self._size * self._image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self._running = False
        self._attack_type = 0

        # get keypresses
        key = pygame.key.get_pressed()

        # can only perform other actions if not currently attacking
        if self._attacking == False and self._alive == True and round_over == False:
            # check player 1 controls
            if self._player == 1:
                # movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self._running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self._running = True
                # jump
                if key[pygame.K_w] and self._jump == False:
                    self._vel_y = -30
                    self._jump = True
                # attack 
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface, target)
                    # determine which attack type is used
                    if key[pygame.K_r]:
                        self._attack_type = 1
                    if key[pygame.K_t]:
                        self._attack_type = 2
            

            # check player 2 controls
            if self._player == 2:
                # movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self._running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self._running = True
                # jump
                if key[pygame.K_UP] and self._jump == False:
                    self._vel_y = -30
                    self._jump = True
                # attack 
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)
                    # determine which attack type is used
                    if key[pygame.K_KP1]:
                        self._attack_type = 1
                    if key[pygame.K_KP2]:
                        self._attack_type = 2

        # apply gravity
        self._vel_y += GRAVITY
        dy += self._vel_y


        # make sure player stays on screen
        if self._rect.left + dx < 0:
            dx = 0
        if self._rect.right + dx > screen_width:
            dx = 0
        if self._rect.bottom + dy > screen_height - 110:
            self._vel_y = 0
            self._jump = False
            dy = screen_height - 110 - self._rect.bottom

        # make sure players face each other
        if target._rect.centerx > self._rect.centerx:
            self._flip = False
        else:
            self._flip = True

        # apply attack cooldown
        if self._attack_cooldown > 0:
            self._attack_cooldown -= 1

        # update player position
        self._rect.x += dx
        self._rect.y += dy

    # handle animation updates
    def update(self):
        # check what action the player is performing
        if self._health <= 0:
            self._health = 0 
            self._alive = False
            self.update_action(2) # death
        elif self._hit == True:
            self.update_action(7) # take hit
        elif self._attacking == True:
            if self._attack_type == 1:
                self.update_action(0) # attack1
            elif self._attack_type == 2:
                self.update_action(1) # attack2
        elif self._jump == True:
            self.update_action(5) # jump
        elif self._running == True:
            self.update_action(6) # running
        else:
            self.update_action(4) # idle
        animation_cooldown = 65
        # update image
        self._image = self._animation_list[self._action][self._frame_index]
        # check if enough time has passed since last update
        if pygame.time.get_ticks() - self._update_time > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()
        # check if animation is finished
        if self._frame_index >= len(self._animation_list[self._action]):
            # check if the fighter is dead and then end the animation (so that it does not reset to idle like the other actions)
            if self._alive == False:
                self._frame_index = len(self._animation_list[self._action]) - 1
            else:
                self._frame_index = 0
                # check if an attack was executed (attack is throw but we have also come to the end of the animation)
                if self._action == 0 or self._action == 1:
                    self._attacking = False
                    self._attack_cooldown = 20
                # check if fighter was hit 
                if self._action == 7:
                    self._hit = False
                    # if both fighters attack at the same time, the attacks cancel out 
                    self._attacking = False
                    self._attack_cooldown = 20


    def attack(self, surface, target):
        if self._attack_cooldown == 0:
            self._attacking = True
            attacking_rect = pygame.Rect(self._rect.centerx - (2 * self._rect.width * self._flip), self._rect.y, 2 * self._rect.width, self._rect.height)
            if attacking_rect.colliderect(target._rect):
                target._health -= 10
                target._hit = True


            #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        # check if new action is different to the previous one 
        if new_action != self._action:
            self._action = new_action
            # update animation settings (reset frame index to 0 when a new action is initiated)
            self._frame_index = 0
            self._update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self._image, self._flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self._rect)
        surface.blit(img, (self._rect.x - (self._offset[0] * self._image_scale), self._rect.y - (self._offset[1] * self._image_scale)))